"""Inventory schemas"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date, datetime
from .enums import BloodGroup, Component


class InventoryBase(BaseModel):
    """Base inventory schema"""
    hospital_id: str = Field(..., min_length=1, max_length=50)
    blood_group: BloodGroup
    component: Component
    units: int = Field(..., gt=0)
    unit_expiry_date: date
    collection_date: date

    @field_validator('unit_expiry_date')
    @classmethod
    def validate_expiry_date(cls, v: date, info) -> date:
        """Validate that expiry date is after collection date"""
        if 'collection_date' in info.data and v < info.data['collection_date']:
            raise ValueError('unit_expiry_date must be after collection_date')
        return v


class InventoryCreate(InventoryBase):
    """Schema for creating inventory record"""
    record_id: str = Field(..., min_length=1, max_length=50)


class InventoryRecord(InventoryBase):
    """Schema for inventory record with ID"""
    record_id: str

    class Config:
        from_attributes = True


class InventoryResponse(InventoryRecord):
    """Schema for inventory response with timestamps"""
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InventoryFilters(BaseModel):
    """Schema for inventory filtering"""
    hospital_id: Optional[str] = None
    blood_group: Optional[BloodGroup] = None
    component: Optional[Component] = None
