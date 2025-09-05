from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, status, Query
from fastapi.responses import FileResponse
from typing import List, Optional
import os
import uuid
import shutil
from pathlib import Path
from PIL import Image
import io

from models import (
    MessageCreate, Message, ConversationSummary, MessagesResponse, 
    MessageType, MessageStatus
)
from models.auth import User
from auth.dependencies import get_current_active_user
from database import database
from datetime import datetime

router = APIRouter(prefix="/api/messages", tags=["messages"])

# Create uploads directory for message images
MESSAGE_UPLOAD_DIR = Path("/app/uploads/messages")
MESSAGE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Image upload settings
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB for message images

def validate_message_image(file: UploadFile) -> bool:
    """Validate uploaded message image"""
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False
    
    if file.size > MAX_FILE_SIZE:
        return False
    
    return True

def resize_message_image(image_data: bytes, max_width: int = 800, max_height: int = 600, quality: int = 85) -> bytes:
    """Resize and optimize message image"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        
        # Resize if necessary
        if image.width > max_width or image.height > max_height:
            image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save optimized image
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        return output.getvalue()
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")

@router.post("/send", response_model=Message)
async def send_message(
    job_id: str = Form(...),
    recipient_id: str = Form(...),
    content: str = Form(...),
    message_type: MessageType = Form(MessageType.TEXT),
    file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_active_user)
):
    """Send a new message in a job conversation"""
    try:
        # Verify job exists and user is authorized (homeowner or quoted tradesperson)
        job = await database.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check if user is authorized to message about this job
        is_job_owner = job.get("homeowner", {}).get("email") == current_user.email
        
        # Check if user is a tradesperson who has submitted a quote
        user_has_quote = False
        if current_user.role == "tradesperson":
            quotes = await database.get_quotes_by_job_id(job_id)
            user_has_quote = any(quote.get("tradesperson_id") == current_user.id for quote in quotes)
        
        if not (is_job_owner or user_has_quote):
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to send messages for this job"
            )
        
        # Verify recipient exists
        recipient = await database.get_user_by_id(recipient_id)
        if not recipient:
            raise HTTPException(status_code=404, detail="Recipient not found")
        
        # Handle image upload if provided
        image_url = None
        image_filename = None
        
        if file and message_type == MessageType.IMAGE:
            if not validate_message_image(file):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid image file. Max size 10MB, formats: JPG, PNG, WebP"
                )
            
            # Read and optimize image
            file_content = await file.read()
            optimized_content = resize_message_image(file_content)
            
            # Save image file
            file_ext = Path(file.filename).suffix.lower()
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = MESSAGE_UPLOAD_DIR / unique_filename
            
            with open(file_path, "wb") as f:
                f.write(optimized_content)
            
            image_url = f"/api/messages/images/{unique_filename}"
            image_filename = unique_filename
        
        # Create message data
        message_data = {
            "id": str(uuid.uuid4()),
            "job_id": job_id,
            "sender_id": current_user.id,
            "recipient_id": recipient_id,
            "content": content,
            "message_type": message_type,
            "image_url": image_url,
            "image_filename": image_filename,
            "status": MessageStatus.SENT,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "read_at": None
        }
        
        # Save to database
        created_message = await database.create_message(message_data)
        
        return Message(**created_message)
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up file if database save fails
        if 'file_path' in locals() and file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send message: {str(e)}"
        )

@router.get("/images/{filename}")
async def get_message_image(filename: str):
    """Serve message images"""
    file_path = MESSAGE_UPLOAD_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(
        path=file_path,
        media_type="image/jpeg",
        headers={"Cache-Control": "public, max-age=3600"}
    )

@router.get("/job/{job_id}", response_model=MessagesResponse)
async def get_job_messages(
    job_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=100),
    current_user: User = Depends(get_current_active_user)
):
    """Get messages for a specific job conversation"""
    try:
        # Verify job exists and user is authorized
        job = await database.get_job_by_id(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Check authorization
        is_job_owner = job.get("homeowner", {}).get("email") == current_user.email
        
        user_has_quote = False
        if current_user.role == "tradesperson":
            quotes = await database.get_quotes_by_job_id(job_id)
            user_has_quote = any(quote.get("tradesperson_id") == current_user.id for quote in quotes)
        
        if not (is_job_owner or user_has_quote):
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to view messages for this job"
            )
        
        # Get messages with pagination
        skip = (page - 1) * limit
        messages = await database.get_job_messages(
            job_id=job_id,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        
        # Get conversation summary
        conversation = await database.get_conversation_summary(job_id, current_user.id)
        
        # Convert messages to Message objects
        message_objects = [Message(**msg) for msg in messages]
        
        # Calculate pagination
        total_messages = await database.get_job_messages_count(job_id)
        total_pages = (total_messages + limit - 1) // limit
        
        return MessagesResponse(
            messages=message_objects,
            conversation=ConversationSummary(**conversation),
            pagination={
                "page": page,
                "limit": limit,
                "total": total_messages,
                "pages": total_pages
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )

@router.get("/conversations", response_model=List[ConversationSummary])
async def get_user_conversations(
    current_user: User = Depends(get_current_active_user)
):
    """Get all job conversations for the current user"""
    try:
        conversations = await database.get_user_conversations(current_user.id)
        return [ConversationSummary(**conv) for conv in conversations]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversations: {str(e)}"
        )

@router.put("/{message_id}/read")
async def mark_message_as_read(
    message_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Mark a message as read"""
    try:
        # Get message and verify user is recipient
        message = await database.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        
        if message["recipient_id"] != current_user.id:
            raise HTTPException(
                status_code=403, 
                detail="Not authorized to mark this message as read"
            )
        
        # Update message status
        await database.mark_message_as_read(message_id)
        
        return {"message": "Message marked as read"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark message as read: {str(e)}"
        )

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_active_user)
):
    """Get total unread messages count for current user"""
    try:
        count = await database.get_unread_messages_count(current_user.id)
        return {"unread_count": count}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get unread count: {str(e)}"
        )