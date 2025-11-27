"""Notification schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .enums import NotificationStatus


class NotificationBase(BaseModel):
    """Base notification schema"""
    donor_id: Optional[int] = None
    template_id: Optional[str] = Field(None, max_length=50)
    message: str = Field(..., min_length=1)


class NotificationCreate(NotificationBase):
    """Schema for creating notification"""
    pass


class NotificationResponse(NotificationBase):
    """Schema for notification response"""
    notification_id: int
    status: NotificationStatus
    sent_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
