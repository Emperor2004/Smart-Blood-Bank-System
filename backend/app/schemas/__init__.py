"""Pydantic schemas for API validation"""
from .enums import BloodGroup, Component, Purpose, TransferStatus, NotificationStatus, UserRole
from .hospital import Hospital, HospitalCreate, HospitalResponse
from .inventory import InventoryRecord, InventoryCreate, InventoryResponse, InventoryFilters
from .usage import UsageRecord, UsageCreate, UsageResponse
from .donor import Donor, DonorCreate, DonorResponse, DonorSearch
from .forecast import ForecastPoint, ForecastResult, ForecastRequest
from .transfer import TransferRecommendation, TransferCreate, TransferResponse, TransferApproval
from .user import User, UserCreate, UserResponse, UserLogin
from .notification import NotificationCreate, NotificationResponse

__all__ = [
    # Enums
    'BloodGroup',
    'Component',
    'Purpose',
    'TransferStatus',
    'NotificationStatus',
    'UserRole',
    # Hospital
    'Hospital',
    'HospitalCreate',
    'HospitalResponse',
    # Inventory
    'InventoryRecord',
    'InventoryCreate',
    'InventoryResponse',
    'InventoryFilters',
    # Usage
    'UsageRecord',
    'UsageCreate',
    'UsageResponse',
    # Donor
    'Donor',
    'DonorCreate',
    'DonorResponse',
    'DonorSearch',
    # Forecast
    'ForecastPoint',
    'ForecastResult',
    'ForecastRequest',
    # Transfer
    'TransferRecommendation',
    'TransferCreate',
    'TransferResponse',
    'TransferApproval',
    # User
    'User',
    'UserCreate',
    'UserResponse',
    'UserLogin',
    # Notification
    'NotificationCreate',
    'NotificationResponse',
]
