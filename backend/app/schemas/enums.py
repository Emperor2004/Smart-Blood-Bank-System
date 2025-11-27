"""Enum definitions for Pydantic schemas"""
from enum import Enum


class BloodGroup(str, Enum):
    """Blood group types"""
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class Component(str, Enum):
    """Blood component types"""
    RBC = "RBC"
    PLATELETS = "Platelets"
    PLASMA = "Plasma"


class Purpose(str, Enum):
    """Usage purpose types"""
    SURGERY = "surgery"
    EMERGENCY = "emergency"
    OTHER = "other"


class TransferStatus(str, Enum):
    """Transfer status types"""
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NotificationStatus(str, Enum):
    """Notification status types"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    SIMULATED = "simulated"


class UserRole(str, Enum):
    """User role types"""
    STAFF = "staff"
    ADMIN = "admin"
