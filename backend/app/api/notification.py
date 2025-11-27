"""Notification API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.notification import NotificationService
from app.services.donor import DonorService
from app.repositories.hospital import HospitalRepository

router = APIRouter()


@router.post("/donor")
def notify_donor(
    donor_id: int = Query(..., description="Donor ID"),
    hospital_id: str = Query(..., description="Hospital ID"),
    blood_group: str = Query(..., description="Blood group needed"),
    db: Session = Depends(get_db)
):
    """
    Send notification to donor.
    
    Args:
        donor_id: Donor ID
        hospital_id: Hospital ID
        blood_group: Blood group needed
        db: Database session
        
    Returns:
        Notification result
    """
    notification_service = NotificationService(db)
    donor_service = DonorService(db)
    hospital_repo = HospitalRepository(db)
    
    # Get donor
    donor = donor_service.get_donor_by_id(donor_id)
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor {donor_id} not found"
        )
    
    # Get hospital
    hospital = hospital_repo.get_by_id(hospital_id)
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hospital {hospital_id} not found"
        )
    
    try:
        result = notification_service.notify_donor(
            donor_id=donor_id,
            donor_phone=donor["phone"],
            hospital_name=hospital.name,
            blood_group=blood_group,
            contact_phone=hospital.contact_phone or "N/A",
            contact_link=f"http://bloodbank.gov.in/contact/{hospital_id}"
        )
        
        return {
            "success": True,
            "notification": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send notification: {str(e)}"
        )


@router.get("")
def get_notifications(
    donor_id: Optional[int] = Query(None, description="Donor ID filter"),
    status_filter: Optional[str] = Query(None, alias="status", description="Status filter"),
    db: Session = Depends(get_db)
):
    """
    Get notification records.
    
    Args:
        donor_id: Optional donor ID filter
        status_filter: Optional status filter
        db: Database session
        
    Returns:
        List of notifications
    """
    notification_service = NotificationService(db)
    
    try:
        notifications = notification_service.get_notifications(
            donor_id=donor_id,
            status=status_filter
        )
        
        return {
            "count": len(notifications),
            "notifications": notifications
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve notifications: {str(e)}"
        )
