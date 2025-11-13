from typing import List, Optional, Literal
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Each class maps to a Mongo collection: class name lowercased

class User(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: Optional[str] = None
    provider: Literal['email', 'google'] = 'email'
    hashed_password: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Project(BaseModel):
    id: Optional[str] = None
    owner_id: str
    title: str
    date: Optional[str] = None
    location: Optional[str] = None
    platform: Optional[str] = None
    mood: Optional[str] = None
    theme_id: Optional[str] = None
    slides: List[dict] = []
    collaborators: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MediaAsset(BaseModel):
    id: Optional[str] = None
    owner_id: str
    project_id: Optional[str] = None
    url: str
    type: Literal['image', 'video']
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ShareLink(BaseModel):
    id: Optional[str] = None
    project_id: str
    token: str
    role: Literal['viewer', 'editor'] = 'viewer'
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

class AuthPayload(BaseModel):
    email: EmailStr
    password: Optional[str] = None
    name: Optional[str] = None

class SlideExportRequest(BaseModel):
    project_id: str
    format: Literal['images', 'video', 'pptx'] = 'images'
