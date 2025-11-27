"""Transfer repository for database operations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.transfer import Transfer


class TransferRepository:
    """Repository for transfer CRUD operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def create(self, transfer_data: dict) -> Transfer:
        """Create a new transfer record."""
        db_transfer = Transfer(
            source_hospital_id=transfer_data["source_hospital_id"],
            destination_hospital_id=transfer_data["destination_hospital_id"],
            blood_group=transfer_data["blood_group"],
            component=transfer_data["component"],
            units=transfer_data["units"],
            urgency_score=transfer_data.get("urgency_score"),
            distance_km=transfer_data.get("distance_km"),
            eta_minutes=transfer_data.get("eta_minutes"),
            status=transfer_data.get("status", "pending"),
            approved_by=transfer_data.get("approved_by")
        )
        self.db.add(db_transfer)
        self.db.commit()
        self.db.refresh(db_transfer)
        return db_transfer
    
    def get_by_id(self, transfer_id: int) -> Optional[Transfer]:
        """Get transfer record by ID."""
        return self.db.query(Transfer).filter(Transfer.transfer_id == transfer_id).first()
    
    def get_all(
        self,
        hospital_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Transfer]:
        """Get all transfer records with optional filters."""
        query = self.db.query(Transfer)
        
        if hospital_id:
            query = query.filter(
                (Transfer.source_hospital_id == hospital_id) |
                (Transfer.destination_hospital_id == hospital_id)
            )
        
        if status:
            query = query.filter(Transfer.status == status)
        
        return query.order_by(Transfer.created_at.desc()).all()
    
    def update_status(
        self,
        transfer_id: int,
        status: str,
        approved_by: Optional[str] = None
    ) -> Optional[Transfer]:
        """Update transfer status."""
        transfer = self.get_by_id(transfer_id)
        if not transfer:
            return None
        
        transfer.status = status
        if approved_by:
            transfer.approved_by = approved_by
        
        self.db.commit()
        self.db.refresh(transfer)
        return transfer
