"""Hospital repository for database operations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.hospital import Hospital
from app.schemas.hospital import HospitalCreate


class HospitalRepository:
    """Repository for hospital CRUD operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, hospital: HospitalCreate) -> Hospital:
        """
        Create a new hospital record.
        
        Args:
            hospital: Hospital data to create
            
        Returns:
            Created hospital record
        """
        db_hospital = Hospital(
            hospital_id=hospital.hospital_id,
            name=hospital.name,
            address=hospital.address,
            latitude=hospital.latitude,
            longitude=hospital.longitude,
            contact_name=hospital.contact_name,
            contact_phone=hospital.contact_phone,
            contact_email=hospital.contact_email
        )
        self.db.add(db_hospital)
        self.db.commit()
        self.db.refresh(db_hospital)
        return db_hospital
    
    def get_by_id(self, hospital_id: str) -> Optional[Hospital]:
        """
        Get hospital record by ID.
        
        Args:
            hospital_id: Hospital ID to retrieve
            
        Returns:
            Hospital record or None if not found
        """
        return self.db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    
    def get_all(self) -> List[Hospital]:
        """
        Get all hospital records.
        
        Returns:
            List of hospital records
        """
        return self.db.query(Hospital).all()
    
    def update(self, hospital_id: str, updates: dict) -> Optional[Hospital]:
        """
        Update a hospital record.
        
        Args:
            hospital_id: Hospital ID to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated hospital record or None if not found
        """
        db_hospital = self.get_by_id(hospital_id)
        if not db_hospital:
            return None
        
        for field, value in updates.items():
            if hasattr(db_hospital, field):
                setattr(db_hospital, field, value)
        
        self.db.commit()
        self.db.refresh(db_hospital)
        return db_hospital
    
    def delete(self, hospital_id: str) -> bool:
        """
        Delete a hospital record.
        
        Args:
            hospital_id: Hospital ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_hospital = self.get_by_id(hospital_id)
        if not db_hospital:
            return False
        
        self.db.delete(db_hospital)
        self.db.commit()
        return True
