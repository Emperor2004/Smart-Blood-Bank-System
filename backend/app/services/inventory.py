"""Inventory service for business logic."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryFilters, InventoryResponse
from app.repositories.inventory import InventoryRepository


class InventoryService:
    """Service for inventory business logic."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.repository = InventoryRepository(db)
    
    def filter_inventory(
        self,
        hospital_id: Optional[str] = None,
        blood_group: Optional[str] = None,
        component: Optional[str] = None
    ) -> List[Inventory]:
        """
        Filter inventory records by multiple criteria.
        
        The filtering is composable - filters can be applied in any order
        and the result will be the same (order-independent).
        
        Args:
            hospital_id: Optional hospital ID filter
            blood_group: Optional blood group filter
            component: Optional component filter
            
        Returns:
            List of inventory records matching all specified criteria
        """
        filters = InventoryFilters(
            hospital_id=hospital_id,
            blood_group=blood_group,
            component=component
        )
        
        return self.repository.get_all(filters)
    
    def get_stock_summary(self, hospital_id: str) -> dict:
        """
        Get stock summary for a hospital.
        
        Args:
            hospital_id: Hospital ID
            
        Returns:
            Dictionary with stock summary by blood group and component
        """
        records = self.filter_inventory(hospital_id=hospital_id)
        
        summary = {}
        for record in records:
            key = f"{record.blood_group}_{record.component}"
            if key not in summary:
                summary[key] = {
                    "blood_group": record.blood_group,
                    "component": record.component,
                    "total_units": 0,
                    "record_count": 0
                }
            summary[key]["total_units"] += record.units
            summary[key]["record_count"] += 1
        
        return {
            "hospital_id": hospital_id,
            "summary": list(summary.values()),
            "total_records": len(records)
        }
