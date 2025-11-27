"""Dashboard API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.expiry import ExpiryService

router = APIRouter()


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """
    Get dashboard summary with key metrics.
    
    Args:
        db: Database session
        
    Returns:
        Dashboard summary with expiry metrics
    """
    expiry_service = ExpiryService(db)
    summary = expiry_service.get_expiry_summary()
    
    return {
        "status": "success",
        "data": summary
    }


@router.get("/high-risk-inventory")
def get_high_risk_inventory(db: Session = Depends(get_db)):
    """
    Get all high-risk inventory units.
    
    Args:
        db: Database session
        
    Returns:
        List of high-risk inventory records
    """
    expiry_service = ExpiryService(db)
    high_risk_units = expiry_service.get_high_risk_units()
    
    return {
        "status": "success",
        "count": len(high_risk_units),
        "data": high_risk_units
    }


@router.get("/inventory-with-risk")
def get_inventory_with_risk(db: Session = Depends(get_db)):
    """
    Get all inventory with risk scores.
    
    Args:
        db: Database session
        
    Returns:
        List of inventory records with risk calculations
    """
    expiry_service = ExpiryService(db)
    inventory_with_risk = expiry_service.get_inventory_with_risk_scores()
    
    return {
        "status": "success",
        "count": len(inventory_with_risk),
        "data": inventory_with_risk
    }
