"""Hospital schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class HospitalBase(BaseModel):
    """Base hospital schema"""
    name: str = Field(..., min_length=1, max_length=255)
    address: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    contact_name: Optional[str] = Field(None, max_length=255)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[str] = Field(None, max_length=255)


class HospitalCreate(HospitalBase):
    """Schema for creating a hospital"""
    hospital_id: str = Field(..., min_length=1, max_length=50)


class Hospital(HospitalBase):
    """Schema for hospital with ID"""
    hospital_id: str

    class Config:
        from_attributes = True


class HospitalResponse(Hospital):
    """Schema for hospital response with timestamps"""
    created_at: datetime

    class Config:
        from_attributes = True
