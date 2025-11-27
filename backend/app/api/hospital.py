"""Hospital API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.repositories.hospital import HospitalRepository
from app.schemas.hospital import HospitalCreate, HospitalResponse

router = APIRouter()


@router.post("", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
def create_hospital(
    hospital: HospitalCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new hospital.
    
    Args:
        hospital: Hospital data to create
        db: Database session
        
    Returns:
        Created hospital record
    """
    repository = HospitalRepository(db)
    
    # Check if hospital already exists
    existing = repository.get_by_id(hospital.hospital_id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Hospital with ID {hospital.hospital_id} already exists"
        )
    
    try:
        record = repository.create(hospital)
        return record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create hospital: {str(e)}"
        )


@router.get("", response_model=List[HospitalResponse])
def get_hospitals(db: Session = Depends(get_db)):
    """
    Get all hospitals.
    
    Args:
        db: Database session
        
    Returns:
        List of hospital records
    """
    repository = HospitalRepository(db)
    hospitals = repository.get_all()
    return hospitals


@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital_by_id(
    hospital_id: str,
    db: Session = Depends(get_db)
):
    """
    Get hospital by ID.
    
    Args:
        hospital_id: Hospital ID to retrieve
        db: Database session
        
    Returns:
        Hospital record
    """
    repository = HospitalRepository(db)
    hospital = repository.get_by_id(hospital_id)
    
    if not hospital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hospital {hospital_id} not found"
        )
    
    return hospital
