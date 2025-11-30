"""e-RaktKosh API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.eraktkosh import ERaktKoshService
from app.repositories.inventory import InventoryRepository

router = APIRouter()


@router.post("/sync/{hospital_id}")
async def sync_inventory(
    hospital_id: str,
    db: Session = Depends(get_db)
):
    """
    Sync inventory from e-RaktKosh API.
    
    Args:
        hospital_id: Hospital ID
        db: Database session
        
    Returns:
        Sync result
    """
    service = ERaktKoshService()
    result = await service.sync_inventory(hospital_id)
    
    if not result["success"]:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=result.get("error", "Failed to sync with e-RaktKosh")
        )
    
    # Save records to database
    if result.get("records"):
        repository = InventoryRepository(db)
        try:
            repository.create_many(result["records"])
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save records: {str(e)}"
            )
    
    return {
        "success": True,
        "hospital_id": hospital_id,
        "records_synced": result["count"]
    }


@router.get("/status")
async def get_status():
    """
    Get e-RaktKosh integration status.
    
    Returns:
        Integration status
    """
    service = ERaktKoshService()
    return {
        "enabled": service.enabled,
        "api_url": service.api_url if service.enabled else None
    }
