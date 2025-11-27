"""Forecast API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.services.forecast import ForecastService

router = APIRouter()


@router.get("")
def get_forecast(
    hospital_id: str = Query(..., description="Hospital ID"),
    blood_group: Optional[str] = Query(None, description="Blood group filter"),
    component: Optional[str] = Query(None, description="Component filter"),
    days: int = Query(7, ge=1, le=30, description="Number of days to forecast"),
    db: Session = Depends(get_db)
):
    """
    Get forecast for hospital, blood group, and component.
    
    Args:
        hospital_id: Hospital ID
        blood_group: Optional blood group filter
        component: Optional component filter
        days: Number of days to forecast (1-30)
        db: Database session
        
    Returns:
        Forecast data with predictions and confidence intervals
    """
    forecast_service = ForecastService(db)
    
    # If blood_group and component are specified, generate forecast
    if blood_group and component:
        try:
            result = forecast_service.generate_forecast(
                hospital_id=hospital_id,
                blood_group=blood_group,
                component=component,
                days=days
            )
            
            if "error" in result:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=result["error"]
                )
            
            return result
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate forecast: {str(e)}"
            )
    else:
        # Get stored forecasts
        try:
            forecasts = forecast_service.get_stored_forecast(
                hospital_id=hospital_id,
                blood_group=blood_group,
                component=component,
                days=days
            )
            
            return {
                "hospital_id": hospital_id,
                "blood_group": blood_group,
                "component": component,
                "count": len(forecasts),
                "forecasts": forecasts
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to retrieve forecasts: {str(e)}"
            )


@router.post("/generate")
def generate_and_store_forecast(
    hospital_id: str = Query(..., description="Hospital ID"),
    blood_group: str = Query(..., description="Blood group"),
    component: str = Query(..., description="Component"),
    days: int = Query(7, ge=1, le=30, description="Number of days to forecast"),
    db: Session = Depends(get_db)
):
    """
    Generate forecast and store in database.
    
    Args:
        hospital_id: Hospital ID
        blood_group: Blood group
        component: Component
        days: Number of days to forecast (1-30)
        db: Database session
        
    Returns:
        Generated forecast data
    """
    forecast_service = ForecastService(db)
    
    try:
        result = forecast_service.generate_and_store_forecast(
            hospital_id=hospital_id,
            blood_group=blood_group,
            component=component,
            days=days
        )
        
        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate and store forecast: {str(e)}"
        )
