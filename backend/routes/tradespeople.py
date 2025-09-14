from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import sys
import os
backend_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, backend_dir)
import models
from database import database
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/tradespeople", tags=["tradespeople"])

@router.post("/", response_model=models.Tradesperson)
async def create_tradesperson(tradesperson_data: models.TradespersonCreate):
    """Register a new tradesperson"""
    try:
        # Check if email already exists
        existing = await database.get_tradesperson_by_email(tradesperson_data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Convert to dict and prepare for database
        tradesperson_dict = tradesperson_data.dict()
        tradesperson_dict['id'] = str(uuid.uuid4())  # Generate new ID
        tradesperson_dict['average_rating'] = 0.0
        tradesperson_dict['total_reviews'] = 0
        tradesperson_dict['total_jobs'] = 0
        tradesperson_dict['verified'] = False
        tradesperson_dict['created_at'] = datetime.utcnow()
        tradesperson_dict['updated_at'] = datetime.utcnow()
        
        # Save to database
        created_tradesperson = await database.create_tradesperson(tradesperson_dict)
        
        return models.Tradesperson(**created_tradesperson)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
async def get_tradespeople(
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50),
    search: Optional[str] = None,
    trade: Optional[str] = None,
    location: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    sort_by: Optional[str] = Query("rating", regex="^(rating|reviews|experience|recent)$")
):
    """Get tradespeople with filters and search"""
    try:
        skip = (page - 1) * limit
        
        # Build filters for users collection where role is tradesperson
        filters = {"role": "tradesperson", "status": "active"}
        
        # Search across name, business_name, bio, profession fields
        if search:
            search_pattern = {"$regex": search, "$options": "i"}
            filters["$or"] = [
                {"name": search_pattern},
                {"business_name": search_pattern},
                {"bio": search_pattern},
                {"profession": search_pattern}
            ]
        
        # Filter by trade/profession
        if trade:
            filters["profession"] = {"$regex": trade, "$options": "i"}
            
        # Filter by location (check city, state, location fields)
        if location:
            location_pattern = {"$regex": location, "$options": "i"}
            filters["$or"] = filters.get("$or", []) + [
                {"city": location_pattern},
                {"state": location_pattern}, 
                {"location": location_pattern}
            ]
        
        # Filter by minimum rating
        if min_rating is not None:
            filters["average_rating"] = {"$gte": min_rating}
        
        # Build sort criteria
        sort_criteria = []
        if sort_by == "rating":
            sort_criteria = [("average_rating", -1), ("total_reviews", -1)]
        elif sort_by == "reviews":
            sort_criteria = [("total_reviews", -1), ("average_rating", -1)]
        elif sort_by == "experience":
            sort_criteria = [("years_experience", -1), ("average_rating", -1)]
        elif sort_by == "recent":
            sort_criteria = [("created_at", -1)]
        else:
            sort_criteria = [("average_rating", -1)]
        
        # Get tradespeople from users collection
        users_collection = database.database.users
        cursor = users_collection.find(filters)
        
        # Apply sorting
        for field, direction in sort_criteria:
            cursor = cursor.sort(field, direction)
            
        # Apply pagination
        cursor = cursor.skip(skip).limit(limit)
        tradespeople_raw = await cursor.to_list(length=limit)
        
        # Get total count
        total_count = await users_collection.count_documents(filters)
        
        # Transform data to match frontend expectations
        tradespeople = []
        for tp in tradespeople_raw:
            # Calculate additional stats if needed
            portfolio_count = await database.database.portfolio.count_documents({"tradesperson_id": tp.get("id", "")})
            reviews_count = await database.database.reviews.count_documents({"reviewee_id": tp.get("id", "")})
            completed_jobs = await database.database.jobs.count_documents({
                "assigned_tradesperson_id": tp.get("id", ""),
                "status": "completed"
            })
            
            # Get average rating from reviews if not stored in user document
            avg_rating = tp.get("average_rating", 0)
            if avg_rating == 0 and reviews_count > 0:
                # Calculate average rating from reviews
                reviews_pipeline = [
                    {"$match": {"reviewee_id": tp.get("id", "")}},
                    {"$group": {"_id": None, "avg_rating": {"$avg": "$rating"}}}
                ]
                rating_result = await database.database.reviews.aggregate(reviews_pipeline).to_list(length=1)
                if rating_result:
                    avg_rating = round(rating_result[0]["avg_rating"], 1)
            
            # Transform to expected format
            tradesperson_data = {
                "id": tp.get("id", ""),
                "name": tp.get("name", ""),
                "email": tp.get("email", ""),
                "phone": tp.get("phone", ""),
                "main_trade": tp.get("profession", ""),  # Map profession to main_trade
                "trade_categories": [tp.get("profession", "")] if tp.get("profession") else [],
                "bio": tp.get("bio", ""),
                "location": tp.get("location", ""),
                "city": tp.get("city", ""),
                "state": tp.get("state", ""),
                "postcode": tp.get("postcode", ""),
                "years_experience": tp.get("years_experience", 0),
                "business_name": tp.get("business_name", ""),
                "profile_image": tp.get("profile_image", ""),
                "average_rating": avg_rating,
                "total_reviews": reviews_count,
                "completed_jobs": completed_jobs,
                "portfolio_items": portfolio_count,
                "is_verified": tp.get("is_verified", False),
                "created_at": tp.get("created_at"),
                "response_time": 2,  # Default response time in hours
                "status": tp.get("status", "active"),
                # Additional computed fields
                "verification_status": "verified" if tp.get("is_verified") else "unverified"
            }
            
            tradespeople.append(tradesperson_data)
        
        # Calculate pagination
        total_pages = (total_count + limit - 1) // limit
        
        return {
            "tradespeople": tradespeople,
            "data": tradespeople,  # Include both for compatibility
            "total": total_count,
            "total_pages": total_pages,
            "current_page": page,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tradespeople: {str(e)}")

@router.get("/{tradesperson_id}", response_model=models.Tradesperson)
async def get_tradesperson(tradesperson_id: str):
    """Get a specific tradesperson by ID"""
    try:
        tradesperson = await database.get_tradesperson_by_id(tradesperson_id)
        if not tradesperson:
            raise HTTPException(status_code=404, detail="Tradesperson not found")
        
        return models.Tradesperson(**tradesperson)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{tradesperson_id}/reviews")
async def get_tradesperson_reviews(
    tradesperson_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20)
):
    """Get reviews for a specific tradesperson"""
    try:
        # Check if tradesperson exists
        tradesperson = await database.get_tradesperson_by_id(tradesperson_id)
        if not tradesperson:
            raise HTTPException(status_code=404, detail="Tradesperson not found")
        
        skip = (page - 1) * limit
        reviews = await database.get_reviews_by_tradesperson(
            tradesperson_id, skip=skip, limit=limit
        )
        
        return {
            "reviews": reviews,
            "tradesperson": tradesperson
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))