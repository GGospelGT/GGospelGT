from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional
from datetime import datetime
import logging
import uuid

from database import database
from models.content import ContentType, ContentStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/public/content", tags=["public_content"])

@router.get("/blog")
async def get_public_blog_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    category: Optional[str] = None,
    search: Optional[str] = None,
    featured_only: bool = False
):
    """Get published blog posts for public consumption"""
    
    try:
        # Build filters for public blog posts
        filters = {
            "content_type": ContentType.BLOG_POST.value,
            "status": ContentStatus.PUBLISHED.value,
            "publish_date": {"$lte": datetime.utcnow()}
        }
        
        # Add optional filters
        if category:
            filters["category"] = category
        
        if featured_only:
            filters["is_featured"] = True
        
        if search:
            filters["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"excerpt": {"$regex": search, "$options": "i"}},
                {"content": {"$regex": search, "$options": "i"}},
                {"tags": {"$in": [search]}}
            ]
        
        # Get blog posts
        blog_posts = await database.get_content_items(filters, skip, limit)
        total_count = await database.get_content_items_count(filters)
        
        # Remove sensitive data and format for public consumption
        public_posts = []
        for post in blog_posts:
            public_post = {
                "id": post["id"],
                "title": post["title"],
                "slug": post["slug"],
                "content": post["content"],
                "excerpt": post.get("excerpt"),
                "featured_image": post.get("featured_image"),
                "gallery_images": post.get("gallery_images", []),
                "category": post["category"],
                "tags": post.get("tags", []),
                "is_featured": post.get("is_featured", False),
                "is_sticky": post.get("is_sticky", False),
                "view_count": post.get("view_count", 0),
                "like_count": post.get("like_count", 0),
                "share_count": post.get("share_count", 0),
                "created_at": post["created_at"],
                "updated_at": post["updated_at"],
                "meta_title": post.get("meta_title"),
                "meta_description": post.get("meta_description"),
                "keywords": post.get("keywords", [])
            }
            public_posts.append(public_post)
        
        return {
            "blog_posts": public_posts,
            "pagination": {
                "skip": skip,
                "limit": limit,
                "total": total_count,
                "has_more": skip + limit < total_count
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting public blog posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog posts")

@router.get("/blog/{slug}")
async def get_blog_post_by_slug(slug: str):
    """Get a specific published blog post by slug"""
    
    try:
        # Get the blog post
        blog_post = await database.get_content_item_by_slug(slug)
        
        if not blog_post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Check if it's a published blog post
        if (blog_post["content_type"] != ContentType.BLOG_POST.value or 
            blog_post["status"] != ContentStatus.PUBLISHED.value):
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Check if publish date has passed
        if blog_post.get("publish_date"):
            publish_date = blog_post["publish_date"]
            if isinstance(publish_date, str):
                publish_date = datetime.fromisoformat(publish_date.replace('Z', '+00:00'))
            if publish_date > datetime.utcnow():
                raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Increment view count
        await database.increment_content_view_count(blog_post["id"])
        
        # Format for public consumption
        public_post = {
            "id": blog_post["id"],
            "title": blog_post["title"],
            "slug": blog_post["slug"],
            "content": blog_post["content"],
            "excerpt": blog_post.get("excerpt"),
            "featured_image": blog_post.get("featured_image"),
            "gallery_images": blog_post.get("gallery_images", []),
            "category": blog_post["category"],
            "tags": blog_post.get("tags", []),
            "is_featured": blog_post.get("is_featured", False),
            "is_sticky": blog_post.get("is_sticky", False),
            "view_count": blog_post.get("view_count", 0) + 1,  # Include the increment
            "like_count": blog_post.get("like_count", 0),
            "share_count": blog_post.get("share_count", 0),
            "created_at": blog_post["created_at"],
            "updated_at": blog_post["updated_at"],
            "meta_title": blog_post.get("meta_title"),
            "meta_description": blog_post.get("meta_description"),
            "keywords": blog_post.get("keywords", [])
        }
        
        return {"blog_post": public_post}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting blog post by slug: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog post")

@router.get("/blog/categories")
async def get_blog_categories():
    """Get all available blog post categories"""
    
    try:
        # Get unique categories from published blog posts
        pipeline = [
            {
                "$match": {
                    "content_type": ContentType.BLOG_POST.value,
                    "status": ContentStatus.PUBLISHED.value
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "count": {"$sum": 1}
                }
            },
            {
                "$sort": {"count": -1}
            }
        ]
        
        categories = []
        async for doc in database.database.content_items.aggregate(pipeline):
            categories.append({
                "category": doc["_id"],
                "post_count": doc["count"]
            })
        
        return {"categories": categories}
        
    except Exception as e:
        logger.error(f"Error getting blog categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch blog categories")

@router.get("/blog/featured")
async def get_featured_blog_posts(limit: int = Query(3, ge=1, le=10)):
    """Get featured blog posts"""
    
    try:
        filters = {
            "content_type": ContentType.BLOG_POST.value,
            "status": ContentStatus.PUBLISHED.value,
            "is_featured": True,
            "publish_date": {"$lte": datetime.utcnow()}
        }
        
        featured_posts = await database.get_content_items(filters, 0, limit)
        
        # Format for public consumption
        public_posts = []
        for post in featured_posts:
            public_post = {
                "id": post["id"],
                "title": post["title"],
                "slug": post["slug"],
                "excerpt": post.get("excerpt"),
                "featured_image": post.get("featured_image"),
                "category": post["category"],
                "tags": post.get("tags", []),
                "view_count": post.get("view_count", 0),
                "like_count": post.get("like_count", 0),
                "created_at": post["created_at"],
                "meta_title": post.get("meta_title"),
                "meta_description": post.get("meta_description")
            }
            public_posts.append(public_post)
        
        return {"featured_posts": public_posts}
        
    except Exception as e:
        logger.error(f"Error getting featured blog posts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch featured blog posts")

@router.post("/blog/{post_id}/like")
async def like_blog_post(post_id: str):
    """Like a blog post (increment like count)"""
    
    try:
        # Get the blog post
        blog_post = await database.get_content_item_by_id(post_id)
        
        if not blog_post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Check if it's a published blog post
        if (blog_post["content_type"] != ContentType.BLOG_POST.value or 
            blog_post["status"] != ContentStatus.PUBLISHED.value):
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Increment like count
        await database.increment_content_like_count(post_id)
        
        return {"message": "Blog post liked successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error liking blog post: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to like blog post")

@router.post("/blog/{post_id}/share")
async def share_blog_post(post_id: str):
    """Share a blog post (increment share count)"""
    
    try:
        # Get the blog post
        blog_post = await database.get_content_item_by_id(post_id)
        
        if not blog_post:
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Check if it's a published blog post
        if (blog_post["content_type"] != ContentType.BLOG_POST.value or 
            blog_post["status"] != ContentStatus.PUBLISHED.value):
            raise HTTPException(status_code=404, detail="Blog post not found")
        
        # Increment share count
        await database.increment_content_share_count(post_id)
        
        return {"message": "Blog post shared successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error sharing blog post: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to share blog post")