"""Transfer schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .enums import BloodGroup, Component, TransferStatus


class TransferBase(BaseModel):
    """Base transfer schema"""
    source_hospital_id: str = Field(..., min_length=1, max_length=50)
    destination_hospital_id: str = Field(..., min_length=1, max_length=50)
    blood_group: BloodGroup
    component: Component
    units: int = Field(..., gt=0)


class TransferCreate(TransferBase):
    """Schema for creating transfer"""
    urgency_score: Optional[float] = None
    distance_km: Optional[float] = Field(None, ge=0)
    eta_minutes: Optional[int] = Field(None, ge=0)


class TransferRecommendation(TransferBase):
    """Schema for transfer recommendation"""
    transfer_id: Optional[int] = None
    source_hospital_name: str
    destination_hospital_name: str
    urgency_score: float
    distance_km: float
    eta_minutes: int
    status: TransferStatus = TransferStatus.PENDING

    class Config:
        from_attributes = True


class TransferResponse(TransferBase):
    """Schema for transfer response"""
    transfer_id: int
    urgency_score: Optional[float] = None
    distance_km: Optional[float] = None
    eta_minutes: Optional[int] = None
    status: TransferStatus
    approved_by: Optional[str] = None
    approved_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TransferApproval(BaseModel):
    """Schema for transfer approval"""
    transfer_id: int
    admin_id: str = Field(..., min_length=1, max_length=50)
