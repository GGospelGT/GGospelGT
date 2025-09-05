from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum

# Enums
class JobStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class QuoteStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

class PortfolioItemCategory(str, Enum):
    PLUMBING = "plumbing"
    ELECTRICAL = "electrical"
    CARPENTRY = "carpentry"
    PAINTING = "painting"
    TILING = "tiling"
    ROOFING = "roofing"
    HEATING_GAS = "heating_gas"
    KITCHEN_FITTING = "kitchen_fitting"
    BATHROOM_FITTING = "bathroom_fitting"
    GARDEN_LANDSCAPING = "garden_landscaping"
    FLOORING = "flooring"
    PLASTERING = "plastering"
    OTHER = "other"

# Base Models
class Homeowner(BaseModel):
    name: str
    email: EmailStr
    phone: str

class Location(BaseModel):
    address: str
    postcode: str
    city: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

# Job Models
class JobCreate(BaseModel):
    title: str = Field(..., min_length=10, max_length=200)
    description: str = Field(..., min_length=50, max_length=2000)
    category: str
    location: str
    postcode: str
    budget_min: Optional[int] = Field(None, ge=0)
    budget_max: Optional[int] = Field(None, ge=0)
    timeline: str
    homeowner_name: str
    homeowner_email: EmailStr
    homeowner_phone: str

class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    category: str
    location: str
    postcode: str
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    timeline: str
    homeowner: Homeowner
    status: JobStatus = JobStatus.ACTIVE
    quotes_count: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        # Convert datetime objects to ISO strings for JSON serialization
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.isoformat()
        return d

# Tradesperson Models
class TradespersonCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str
    trade_categories: List[str]
    location: str
    postcode: str
    experience_years: int = Field(..., ge=0, le=50)
    company_name: Optional[str] = None
    description: str = Field(..., min_length=50, max_length=1000)
    certifications: List[str] = []

class Tradesperson(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str
    trade_categories: List[str]
    location: str
    postcode: str
    experience_years: int
    company_name: Optional[str] = None
    description: str
    certifications: List[str] = []
    profile_image: Optional[str] = None
    average_rating: float = 0.0
    total_reviews: int = 0
    total_jobs: int = 0
    verified: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.isoformat()
        return d

# Quote Models
class QuoteCreate(BaseModel):
    job_id: str
    tradesperson_id: Optional[str] = None  # Will be set by backend from auth
    price: int = Field(..., ge=0)
    message: str = Field(..., min_length=20, max_length=1000)
    estimated_duration: str
    start_date: datetime

class Quote(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str
    tradesperson_id: str
    price: int
    message: str
    estimated_duration: str
    start_date: datetime
    status: QuoteStatus = QuoteStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.isoformat()
        return d

# Review Models
class ReviewCreate(BaseModel):
    job_id: str
    tradesperson_id: str
    rating: int = Field(..., ge=1, le=5)
    title: str = Field(..., min_length=5, max_length=100)
    comment: str = Field(..., min_length=10, max_length=1000)
    homeowner_name: str

class Review(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str
    tradesperson_id: str
    rating: int
    title: str
    comment: str
    homeowner_name: str
    location: str
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def dict(self, **kwargs):
        d = super().dict(**kwargs)
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = value.isoformat()
        return d

# Response Models
class JobsResponse(BaseModel):
    jobs: List[Job]
    pagination: dict

class TradespeopleResponse(BaseModel):
    tradespeople: List[Tradesperson]
    total: int

class QuotesResponse(BaseModel):
    quotes: List[Quote]
    job: Job

class ReviewsResponse(BaseModel):
    reviews: List[Review]
    pagination: dict

class StatsResponse(BaseModel):
    total_tradespeople: int
    total_categories: int
    total_reviews: int
    average_rating: float
    total_jobs: int
    active_jobs: int

# Category Model
class Category(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    icon: str
    color: str
    tradesperson_count: int = 0
    avg_price_range: str = ""

# Portfolio Models
class PortfolioItemCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: PortfolioItemCategory
    image_url: str
    image_filename: str

class PortfolioItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tradesperson_id: str
    title: str
    description: Optional[str] = None
    category: PortfolioItemCategory
    image_url: str
    image_filename: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_public: bool = True

class PortfolioResponse(BaseModel):
    items: List[PortfolioItem]
    total: int

# Message Models
class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"

class MessageStatus(str, Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class MessageCreate(BaseModel):
    job_id: str
    recipient_id: str
    content: str
    message_type: MessageType = MessageType.TEXT
    image_url: Optional[str] = None
    image_filename: Optional[str] = None

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    job_id: str
    sender_id: str
    recipient_id: str
    content: str
    message_type: MessageType
    image_url: Optional[str] = None
    image_filename: Optional[str] = None
    status: MessageStatus = MessageStatus.SENT
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None

class ConversationSummary(BaseModel):
    job_id: str
    job_title: str
    other_user_id: str
    other_user_name: str
    other_user_role: str
    last_message: Optional[Message] = None
    unread_count: int = 0
    created_at: datetime
    updated_at: datetime

class MessagesResponse(BaseModel):
    messages: List[Message]
    conversation: ConversationSummary
    pagination: dict