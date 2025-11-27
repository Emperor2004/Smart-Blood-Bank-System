"""Expiry risk calculation service."""
from datetime import date, timedelta
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.inventory import Inventory
from app.repositories.inventory import InventoryRepository
from app.config import settings


class ExpiryService:
    """Service for expiry risk calculations."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.repository = InventoryRepository(db)
        self.threshold_days = settings.expiry_risk_threshold_days
    
    def calculate_days_to_expiry(self, expiry_date: date) -> int:
        """
        Calculate days until expiry.
        
        Args:
            expiry_date: Unit expiry date
            
        Returns:
            Number of days until expiry (negative if expired)
        """
        return (expiry_date - date.today()).days
    
    def calculate_expiry_risk_score(self, expiry_date: date, units: int) -> float:
        """
        Calculate expiry risk score.
        
        Formula: risk_score = (1 / (days_to_expiry + 1)) * units
        
        Args:
            expiry_date: Unit expiry date
            units: Number of units
            
        Returns:
            Expiry risk score
        """
        days_to_expiry = self.calculate_days_to_expiry(expiry_date)
        risk_score = (1.0 / (days_to_expiry + 1)) * units
        return risk_score
    
    def is_high_risk(self, expiry_date: date, threshold_days: int = None) -> bool:
        """
        Check if unit is high risk based on expiry date.
        
        Args:
            expiry_date: Unit expiry date
            threshold_days: Optional custom threshold (uses config default if not provided)
            
        Returns:
            True if high risk, False otherwise
        """
        if threshold_days is None:
            threshold_days = self.threshold_days
        
        days_to_expiry = self.calculate_days_to_expiry(expiry_date)
        return days_to_expiry <= threshold_days
    
    def get_high_risk_units(self, threshold_days: int = None) -> List[Inventory]:
        """
        Get all high-risk inventory units.
        
        Args:
            threshold_days: Optional custom threshold (uses config default if not provided)
            
        Returns:
            List of high-risk inventory records
        """
        if threshold_days is None:
            threshold_days = self.threshold_days
        
        return self.repository.get_by_expiry_range(threshold_days)
    
    def get_expiry_summary(self) -> Dict:
        """
        Get summary of expiry risk across all inventory.
        
        Returns:
            Dictionary with expiry summary statistics
        """
        # Get all inventory
        all_inventory = self.repository.get_all()
        
        # Get high-risk units
        high_risk_units = self.get_high_risk_units()
        
        # Calculate statistics
        total_units = sum(record.units for record in all_inventory)
        high_risk_count = len(high_risk_units)
        high_risk_total_units = sum(record.units for record in high_risk_units)
        
        # Calculate units near expiry by days
        units_expiring_today = 0
        units_expiring_tomorrow = 0
        units_expiring_3_days = 0
        units_expiring_7_days = 0
        
        today = date.today()
        
        for record in all_inventory:
            days_to_expiry = self.calculate_days_to_expiry(record.unit_expiry_date)
            
            if days_to_expiry == 0:
                units_expiring_today += record.units
            if days_to_expiry <= 1:
                units_expiring_tomorrow += record.units
            if days_to_expiry <= 3:
                units_expiring_3_days += record.units
            if days_to_expiry <= 7:
                units_expiring_7_days += record.units
        
        return {
            "total_units": total_units,
            "total_records": len(all_inventory),
            "high_risk_count": high_risk_count,
            "high_risk_units": high_risk_total_units,
            "units_expiring_today": units_expiring_today,
            "units_expiring_tomorrow": units_expiring_tomorrow,
            "units_expiring_3_days": units_expiring_3_days,
            "units_expiring_7_days": units_expiring_7_days,
            "threshold_days": self.threshold_days
        }
    
    def get_inventory_with_risk_scores(self) -> List[Dict]:
        """
        Get all inventory with calculated risk scores.
        
        Returns:
            List of inventory records with risk scores
        """
        all_inventory = self.repository.get_all()
        
        results = []
        for record in all_inventory:
            days_to_expiry = self.calculate_days_to_expiry(record.unit_expiry_date)
            risk_score = self.calculate_expiry_risk_score(record.unit_expiry_date, record.units)
            is_high_risk = self.is_high_risk(record.unit_expiry_date)
            
            results.append({
                "record_id": record.record_id,
                "hospital_id": record.hospital_id,
                "blood_group": record.blood_group,
                "component": record.component,
                "units": record.units,
                "unit_expiry_date": record.unit_expiry_date,
                "collection_date": record.collection_date,
                "days_to_expiry": days_to_expiry,
                "expiry_risk_score": round(risk_score, 4),
                "is_high_risk": is_high_risk
            })
        
        return results
