"""Inventory API endpoints."""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.repositories.inventory import InventoryRepository
from app.services.ingestion import IngestionService
from app.schemas.inventory import (
    InventoryCreate,
    InventoryResponse,
    InventoryFilters
)

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_200_OK)
async def upload_inventory_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process inventory CSV file.
    
    Args:
        file: CSV file to upload
        db: Database session
        
    Returns:
        Upload result with success count and errors
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    
    try:
        # Read file content
        content = await file.read()
        file_content = content.decode('utf-8')
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read file: {str(e)}"
        )
    
    # Parse and validate CSV
    ingestion_service = IngestionService()
    result = ingestion_service.parse_csv(file_content)
    
    # If there are valid records, save them to database
    if result.valid_records:
        repository = InventoryRepository(db)
        try:
            repository.create_many(result.valid_records)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save records to database: {str(e)}"
            )
    
    # Return result
    return {
        "success": result.success_count > 0,
        "message": f"Processed {result.success_count + result.error_count} rows",
        "success_count": result.success_count,
        "error_count": result.error_count,
        "errors": result.errors,
        "duplicates": result.duplicates
    }


@router.post("", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory(
    inventory: InventoryCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new inventory record manually.
    
    Args:
        inventory: Inventory data to create
        db: Database session
        
    Returns:
        Created inventory record
    """
    repository = InventoryRepository(db)
    
    # Check if record already exists
    if repository.exists(inventory.record_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Inventory record with ID {inventory.record_id} already exists"
        )
    
    try:
        record = repository.create(inventory)
        return record
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create inventory record: {str(e)}"
        )


@router.get("", response_model=List[InventoryResponse])
def get_inventory(
    hospital_id: str = None,
    blood_group: str = None,
    component: str = None,
    db: Session = Depends(get_db)
):
    """
    Get inventory records with optional filtering.
    
    Args:
        hospital_id: Optional hospital ID filter
        blood_group: Optional blood group filter
        component: Optional component filter
        db: Database session
        
    Returns:
        List of inventory records
    """
    # Build filters
    filters = InventoryFilters(
        hospital_id=hospital_id,
        blood_group=blood_group,
        component=component
    )
    
    # Get records
    repository = InventoryRepository(db)
    records = repository.get_all(filters)
    
    return records


@router.get("/{record_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    record_id: str,
    db: Session = Depends(get_db)
):
    """
    Get inventory record by ID.
    
    Args:
        record_id: Record ID to retrieve
        db: Database session
        
    Returns:
        Inventory record
    """
    repository = InventoryRepository(db)
    record = repository.get_by_id(record_id)
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record {record_id} not found"
        )
    
    return record
