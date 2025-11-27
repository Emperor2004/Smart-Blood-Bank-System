"""Transfer API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.transfer import TransferService

router = APIRouter()


@router.get("")
def get_transfers(
    hospital_id: Optional[str] = Query(None, description="Hospital ID filter"),
    status_filter: Optional[str] = Query(None, alias="status", description="Status filter"),
    db: Session = Depends(get_db)
):
    """Get transfer records with optional filters."""
    transfer_service = TransferService(db)
    transfers = transfer_service.transfer_repo.get_all(
        hospital_id=hospital_id,
        status=status_filter
    )
    
    return {
        "count": len(transfers),
        "transfers": transfers
    }


@router.get("/recommendations")
def get_transfer_recommendations(
    hospital_id: Optional[str] = Query(None, description="Hospital ID filter"),
    db: Session = Depends(get_db)
):
    """Get transfer recommendations."""
    transfer_service = TransferService(db)
    
    try:
        recommendations = transfer_service.generate_recommendations(hospital_id)
        
        return {
            "count": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recommendations: {str(e)}"
        )


@router.post("/approve")
def approve_transfer(
    source_hospital_id: str = Query(...),
    destination_hospital_id: str = Query(...),
    blood_group: str = Query(...),
    component: str = Query(...),
    units: int = Query(..., gt=0),
    approved_by: str = Query(...),
    db: Session = Depends(get_db)
):
    """Approve and execute transfer."""
    transfer_service = TransferService(db)
    
    try:
        transfer = transfer_service.approve_transfer(
            source_hospital_id=source_hospital_id,
            destination_hospital_id=destination_hospital_id,
            blood_group=blood_group,
            component=component,
            units=units,
            approved_by=approved_by
        )
        
        return {
            "success": True,
            "transfer": transfer
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to approve transfer: {str(e)}"
        )
