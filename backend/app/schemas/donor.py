"""Donor schemas"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime
from .enums import BloodGroup


class DonorBase(BaseModel):
    """Base donor schema"""
    name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    blood_group: BloodGroup
    last_donation_date: Optional[date] = None
    eligible: bool = True
    location_lat: Optional[float] = Field(None, ge=-90, le=90)
    location_lon: Optional[float] = Field(None, ge=-180, le=180)


class DonorCreate(DonorBase):
    """Schema for creating donor"""
    pass


class Donor(DonorBase):
    """Schema for donor with ID"""
    donor_id: int

    class Config:
        from_attributes = True


class DonorResponse(Donor):
    """Schema for donor response with timestamps"""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DonorSearch(BaseModel):
    """Schema for donor search filters"""
    blood_group: Optional[BloodGroup] = None
    radius_km: Optional[float] = Field(None, gt=0)
    eligible_only: bool = False
    hospital_lat: Optional[float] = Field(None, ge=-90, le=90)
    hospital_lon: Optional[float] = Field(None, ge=-180, le=180)
