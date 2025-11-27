"""Inventory repository for database operations."""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate, InventoryFilters
from datetime import date


class InventoryRepository:
    """Repository for inventory CRUD operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, inventory: InventoryCreate) -> Inventory:
        """
        Create a new inventory record.
        
        Args:
            inventory: Inventory data to create
            
        Returns:
            Created inventory record
        """
        db_inventory = Inventory(
            record_id=inventory.record_id,
            hospital_id=inventory.hospital_id,
            blood_group=inventory.blood_group.value,
            component=inventory.component.value,
            units=inventory.units,
            unit_expiry_date=inventory.unit_expiry_date,
            collection_date=inventory.collection_date
        )
        self.db.add(db_inventory)
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory
    
    def create_many(self, inventories: List[InventoryCreate]) -> List[Inventory]:
        """
        Create multiple inventory records in bulk.
        
        Args:
            inventories: List of inventory data to create
            
        Returns:
            List of created inventory records
        """
        db_inventories = []
        for inventory in inventories:
            db_inventory = Inventory(
                record_id=inventory.record_id,
                hospital_id=inventory.hospital_id,
                blood_group=inventory.blood_group.value,
                component=inventory.component.value,
                units=inventory.units,
                unit_expiry_date=inventory.unit_expiry_date,
                collection_date=inventory.collection_date
            )
            db_inventories.append(db_inventory)
        
        self.db.bulk_save_objects(db_inventories, return_defaults=True)
        self.db.commit()
        return db_inventories
    
    def get_by_id(self, record_id: str) -> Optional[Inventory]:
        """
        Get inventory record by ID.
        
        Args:
            record_id: Record ID to retrieve
            
        Returns:
            Inventory record or None if not found
        """
        return self.db.query(Inventory).filter(Inventory.record_id == record_id).first()
    
    def get_all(self, filters: Optional[InventoryFilters] = None) -> List[Inventory]:
        """
        Get all inventory records with optional filtering.
        
        Args:
            filters: Optional filters to apply
            
        Returns:
            List of inventory records
        """
        query = self.db.query(Inventory)
        
        if filters:
            conditions = []
            
            if filters.hospital_id:
                conditions.append(Inventory.hospital_id == filters.hospital_id)
            
            if filters.blood_group:
                conditions.append(Inventory.blood_group == filters.blood_group.value)
            
            if filters.component:
                conditions.append(Inventory.component == filters.component.value)
            
            if conditions:
                query = query.filter(and_(*conditions))
        
        return query.all()
    
    def update(self, record_id: str, updates: dict) -> Optional[Inventory]:
        """
        Update an inventory record.
        
        Args:
            record_id: Record ID to update
            updates: Dictionary of fields to update
            
        Returns:
            Updated inventory record or None if not found
        """
        db_inventory = self.get_by_id(record_id)
        if not db_inventory:
            return None
        
        # Update allowed fields
        allowed_fields = ['units', 'unit_expiry_date', 'collection_date', 'blood_group', 'component']
        for field, value in updates.items():
            if field in allowed_fields and hasattr(db_inventory, field):
                # Convert enum values if needed
                if field in ['blood_group', 'component'] and hasattr(value, 'value'):
                    value = value.value
                setattr(db_inventory, field, value)
        
        self.db.commit()
        self.db.refresh(db_inventory)
        return db_inventory
    
    def delete(self, record_id: str) -> bool:
        """
        Delete an inventory record.
        
        Args:
            record_id: Record ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        db_inventory = self.get_by_id(record_id)
        if not db_inventory:
            return False
        
        self.db.delete(db_inventory)
        self.db.commit()
        return True
    
    def get_by_expiry_range(self, days: int) -> List[Inventory]:
        """
        Get inventory records expiring within specified days.
        
        Args:
            days: Number of days from today
            
        Returns:
            List of inventory records expiring within the range
        """
        from datetime import timedelta
        cutoff_date = date.today() + timedelta(days=days)
        
        return self.db.query(Inventory).filter(
            Inventory.unit_expiry_date <= cutoff_date,
            Inventory.unit_expiry_date >= date.today()
        ).all()
    
    def exists(self, record_id: str) -> bool:
        """
        Check if a record exists.
        
        Args:
            record_id: Record ID to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(Inventory).filter(Inventory.record_id == record_id).count() > 0
