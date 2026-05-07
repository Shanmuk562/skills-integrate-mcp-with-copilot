"""
Data models for activities and registrations
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Activity(BaseModel):
    """Activity model"""
    name: str
    description: str
    schedule: str
    max_participants: int
    participants: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        extra = "forbid"


class ActivityResponse(BaseModel):
    """Activity response model"""
    name: str
    description: str
    schedule: str
    max_participants: int
    participants: List[str]
    participant_count: int


class Registration(BaseModel):
    """Registration model"""
    activity_name: str
    email: str
    registered_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        extra = "forbid"


class SignupRequest(BaseModel):
    """Signup request model"""
    email: str

    class Config:
        extra = "forbid"
