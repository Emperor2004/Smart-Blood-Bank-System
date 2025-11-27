"""Forecast schemas"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date, datetime
from .enums import BloodGroup, Component


class ForecastPoint(BaseModel):
    """Schema for a single forecast point"""
    date: date
    predicted: float = Field(..., ge=0)
    lower: float = Field(..., ge=0)
    upper: float = Field(..., ge=0)


class ForecastResult(BaseModel):
    """Schema for forecast result"""
    hospital_id: str
    blood_group: BloodGroup
    component: Component
    forecast: List[ForecastPoint]
    generated_at: datetime

    class Config:
        from_attributes = True


class ForecastRequest(BaseModel):
    """Schema for forecast request"""
    hospital_id: str = Field(..., min_length=1, max_length=50)
    blood_group: Optional[BloodGroup] = None
    component: Optional[Component] = None
    days: int = Field(7, ge=1, le=365)
