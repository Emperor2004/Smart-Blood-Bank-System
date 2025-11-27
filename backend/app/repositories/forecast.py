"""Forecast repository for database operations."""
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from app.models.forecast import Forecast


class ForecastRepository:
    """Repository for forecast CRUD operations."""
    
    def __init__(self, db: Session):
        """
        Initialize repository with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
    
    def create(self, forecast_data: dict) -> Forecast:
        """
        Create a new forecast record.
        
        Args:
            forecast_data: Dictionary with forecast data
            
        Returns:
            Created forecast record
        """
        db_forecast = Forecast(
            hospital_id=forecast_data["hospital_id"],
            blood_group=forecast_data["blood_group"],
            component=forecast_data["component"],
            forecast_date=forecast_data["forecast_date"],
            predicted_units=forecast_data["predicted_units"],
            lower_bound=forecast_data.get("lower_bound"),
            upper_bound=forecast_data.get("upper_bound")
        )
        self.db.add(db_forecast)
        self.db.commit()
        self.db.refresh(db_forecast)
        return db_forecast
    
    def get_by_id(self, forecast_id: int) -> Optional[Forecast]:
        """
        Get forecast record by ID.
        
        Args:
            forecast_id: Forecast ID to retrieve
            
        Returns:
            Forecast record or None if not found
        """
        return self.db.query(Forecast).filter(Forecast.forecast_id == forecast_id).first()
    
    def get_by_hospital(
        self,
        hospital_id: str,
        blood_group: Optional[str] = None,
        component: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Forecast]:
        """
        Get forecast records for a hospital.
        
        Args:
            hospital_id: Hospital ID
            blood_group: Optional blood group filter
            component: Optional component filter
            start_date: Optional start date filter
            end_date: Optional end date filter
            
        Returns:
            List of forecast records
        """
        query = self.db.query(Forecast).filter(Forecast.hospital_id == hospital_id)
        
        if blood_group:
            query = query.filter(Forecast.blood_group == blood_group)
        if component:
            query = query.filter(Forecast.component == component)
        if start_date:
            query = query.filter(Forecast.forecast_date >= start_date)
        if end_date:
            query = query.filter(Forecast.forecast_date <= end_date)
        
        return query.order_by(Forecast.forecast_date).all()
    
    def get_latest_forecasts(
        self,
        hospital_id: str,
        days: int = 7
    ) -> List[Forecast]:
        """
        Get latest forecasts for a hospital.
        
        Args:
            hospital_id: Hospital ID
            days: Number of days to retrieve
            
        Returns:
            List of latest forecast records
        """
        from datetime import timedelta
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        return self.get_by_hospital(
            hospital_id=hospital_id,
            start_date=start_date,
            end_date=end_date
        )
    
    def delete_old_forecasts(self, days_old: int = 30) -> int:
        """
        Delete forecasts older than specified days.
        
        Args:
            days_old: Number of days to keep
            
        Returns:
            Number of records deleted
        """
        from datetime import timedelta
        cutoff_date = date.today() - timedelta(days=days_old)
        
        count = self.db.query(Forecast).filter(
            Forecast.forecast_date < cutoff_date
        ).delete()
        
        self.db.commit()
        return count
