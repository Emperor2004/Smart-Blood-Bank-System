"""Donor API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.donor import DonorService
from app.schemas.donor import DonorCreate

router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
def register_donor(
    donor: DonorCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new donor.
    
    Args:
        donor: Donor data
        db: Database session
        
    Returns:
        Created donor record
    """
    donor_service = DonorService(db)
    
    try:
        result = donor_service.register_donor(donor)
        return {
            "success": True,
            "donor": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register donor: {str(e)}"
        )


@router.get("/search")
def search_donors(
    blood_group: Optional[str] = Query(None, description="Blood group filter"),
    eligible_only: bool = Query(False, description="Filter for eligible donors only"),
    hospital_lat: Optional[float] = Query(None, description="Hospital latitude"),
    hospital_lon: Optional[float] = Query(None, description="Hospital longitude"),
    radius_km: Optional[float] = Query(None, description="Search radius in km"),
    db: Session = Depends(get_db)
):
    """
    Search for donors with filters.
    
    Args:
        blood_group: Optional blood group filter
        eligible_only: Filter for eligible donors only
        hospital_lat: Hospital latitude for radius search
        hospital_lon: Hospital longitude for radius search
        radius_km: Search radius in kilometers
        db: Database session
        
    Returns:
        List of matching donors
    """
    donor_service = DonorService(db)
    
    try:
        donors = donor_service.search_donors(
            blood_group=blood_group,
            eligible_only=eligible_only,
            hospital_lat=hospital_lat,
            hospital_lon=hospital_lon,
            radius_km=radius_km
        )
        
        return {
            "count": len(donors),
            "donors": donors
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search donors: {str(e)}"
        )


@router.get("/{donor_id}")
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get donor by ID.
    
    Args:
        donor_id: Donor ID
        db: Database session
        
    Returns:
        Donor record
    """
    donor_service = DonorService(db)
    donor = donor_service.get_donor_by_id(donor_id)
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor {donor_id} not found"
        )
    
    return donor


@router.put("/{donor_id}/eligibility")
def update_donor_eligibility(
    donor_id: int,
    db: Session = Depends(get_db)
):
    """
    Update donor eligibility.
    
    Args:
        donor_id: Donor ID
        db: Database session
        
    Returns:
        Updated donor record
    """
    donor_service = DonorService(db)
    donor = donor_service.update_eligibility(donor_id)
    
    if not donor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Donor {donor_id} not found"
        )
    
    return {
        "success": True,
        "donor": donor
    }
