"""User schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .enums import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=1, max_length=100)
    role: UserRole
    hospital_id: Optional[str] = Field(None, max_length=50)


class UserCreate(UserBase):
    """Schema for creating user"""
    user_id: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8)


class User(UserBase):
    """Schema for user with ID"""
    user_id: str

    class Config:
        from_attributes = True


class UserResponse(User):
    """Schema for user response with timestamps"""
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """Schema for user login"""
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1)
