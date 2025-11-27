"""Usage schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from .enums import BloodGroup, Component, Purpose


class UsageBase(BaseModel):
    """Base usage schema"""
    hospital_id: str = Field(..., min_length=1, max_length=50)
    blood_group: BloodGroup
    component: Component
    units_used: int = Field(..., gt=0)
    usage_date: date
    purpose: Optional[Purpose] = None


class UsageCreate(UsageBase):
    """Schema for creating usage record"""
    pass


class UsageRecord(UsageBase):
    """Schema for usage record with ID"""
    usage_id: int

    class Config:
        from_attributes = True


class UsageResponse(UsageRecord):
    """Schema for usage response with timestamps"""
    created_at: datetime

    class Config:
        from_attributes = True
