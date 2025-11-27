"""Usage repository for database operations."""
from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.usage import Usage
from app.schemas.usage import UsageCreate


class UsageRepository:
    """Repository for usage CRUD operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, usage: UsageCreate) -> Usage:
        """
        Create a new usage record.
        
        Args:
            usage: Usage data to create
            
        Returns:
            Created usage record
        """
        db_usage = Usage(
            hospital_id=usage.hospital_id,
            blood_group=usage.blood_group.value,
            component=usage.component.value,
            units_used=usage.units_used,
            usage_date=usage.usage_date,
            purpose=usage.purpose.value if usage.purpose else None
        )
        self.db.add(db_usage)
        self.db.commit()
        self.db.refresh(db_usage)
        return db_usage
    
    def create_many(self, usages: List[UsageCreate]) -> List[Usage]:
        """
        Create multiple usage records in bulk.
        
        Args:
            usages: List of usage data to create
            
        Returns:
            List of created usage records
        """
        db_usages = []
        for usage in usages:
            db_usage = Usage(
                hospital_id=usage.hospital_id,
                blood_group=usage.blood_group.value,
                component=usage.component.value,
                units_used=usage.units_used,
                usage_date=usage.usage_date,
                purpose=usage.purpose.value if usage.purpose else None
            )
            db_usages.append(db_usage)
        
        self.db.bulk_save_objects(db_usages, return_defaults=True)
        self.db.commit()
        return db_usages
    
    def get_by_id(self, usage_id: int) -> Optional[Usage]:
        """
        Get usage record by ID.
        
        Args:
            usage_id: Usage ID to retrieve
            
        Returns:
            Usage record or None if not found
        """
        return self.db.query(Usage).filter(Usage.usage_id == usage_id).first()
    
    def get_by_hospital(
        self,
        hospital_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Usage]:
        """
        Get usage records for a hospital within date range.
        
        Args:
            hospital_id: Hospital ID
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of usage records
        """
        query = self.db.query(Usage).filter(Usage.hospital_id == hospital_id)
        
        if start_date:
            query = query.filter(Usage.usage_date >= start_date)
        if end_date:
            query = query.filter(Usage.usage_date <= end_date)
        
        return query.order_by(Usage.usage_date).all()
    
    def get_aggregated_daily(
        self,
        hospital_id: str,
        blood_group: Optional[str] = None,
        component: Optional[str] = None,
        days: int = 180
    ) -> List[dict]:
        """
        Get daily aggregated usage data.
        
        Args:
            hospital_id: Hospital ID
            blood_group: Optional blood group filter
            component: Optional component filter
            days: Number of days to look back (default 180)
            
        Returns:
            List of dictionaries with aggregated daily usage
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        query = self.db.query(
            Usage.usage_date,
            Usage.blood_group,
            Usage.component,
            func.sum(Usage.units_used).label('total_units')
        ).filter(
            Usage.hospital_id == hospital_id,
            Usage.usage_date >= start_date,
            Usage.usage_date <= end_date
        )
        
        if blood_group:
            query = query.filter(Usage.blood_group == blood_group)
        if component:
            query = query.filter(Usage.component == component)
        
        query = query.group_by(
            Usage.usage_date,
            Usage.blood_group,
            Usage.component
        ).order_by(Usage.usage_date)
        
        results = query.all()
        
        return [
            {
                "date": result.usage_date,
                "blood_group": result.blood_group,
                "component": result.component,
                "units": result.total_units
            }
            for result in results
        ]
    
    def get_all(self) -> List[Usage]:
        """
        Get all usage records.
        
        Returns:
            List of usage records
        """
        return self.db.query(Usage).all()
