"""Forecasting service using Prophet."""
import pandas as pd
import numpy as np
from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from prophet import Prophet
from app.repositories.usage import UsageRepository
from app.repositories.forecast import ForecastRepository
from app.config import settings


class ForecastService:
    """Service for demand forecasting using Prophet."""
    
    def __init__(self, db: Session):
        """
        Initialize service with database session.
        
        Args:
            db: SQLAlchemy database session
        """
        self.db = db
        self.usage_repo = UsageRepository(db)
        self.forecast_repo = ForecastRepository(db)
        self.history_days = settings.forecast_history_days
        self.confidence_interval = settings.forecast_confidence_interval
    
    def preprocess_data(
        self,
        usage_data: List[dict],
        start_date: date,
        end_date: date
    ) -> pd.DataFrame:
        """
        Preprocess usage data for forecasting.
        
        Fills missing dates with zero units and creates continuous daily series.
        
        Args:
            usage_data: List of usage records
            start_date: Start date for series
            end_date: End date for series
            
        Returns:
            DataFrame with continuous daily series
        """
        # Convert to DataFrame
        if not usage_data:
            # Create empty DataFrame with date range
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            df = pd.DataFrame({
                'ds': date_range,
                'y': 0
            })
            return df
        
        df = pd.DataFrame(usage_data)
        df['ds'] = pd.to_datetime(df['date'])
        df['y'] = df['units']
        
        # Create complete date range
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        complete_df = pd.DataFrame({'ds': date_range})
        
        # Merge with actual data, filling missing dates with 0
        merged_df = complete_df.merge(df[['ds', 'y']], on='ds', how='left')
        merged_df['y'] = merged_df['y'].fillna(0)
        
        return merged_df
    
    def train_test_split(
        self,
        df: pd.DataFrame,
        test_days: int = 30
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into train and test sets.
        
        Args:
            df: DataFrame with time series data
            test_days: Number of days for test set (default 30)
            
        Returns:
            Tuple of (train_df, test_df)
        """
        if len(df) <= test_days:
            # Not enough data for split, use all for training
            return df, pd.DataFrame(columns=df.columns)
        
        split_index = len(df) - test_days
        train_df = df.iloc[:split_index].copy()
        test_df = df.iloc[split_index:].copy()
        
        return train_df, test_df
    
    def train_model(self, train_df: pd.DataFrame) -> Prophet:
        """
        Train Prophet model on historical data.
        
        Args:
            train_df: Training data DataFrame
            
        Returns:
            Trained Prophet model
        """
        model = Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=False,
            interval_width=self.confidence_interval
        )
        
        # Suppress Prophet's verbose output
        import logging
        logging.getLogger('prophet').setLevel(logging.WARNING)
        logging.getLogger('cmdstanpy').setLevel(logging.WARNING)
        
        model.fit(train_df)
        return model
    
    def evaluate_model(
        self,
        model: Prophet,
        test_df: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Evaluate model performance on test set.
        
        Calculates MAE and MAPE metrics.
        
        Args:
            model: Trained Prophet model
            test_df: Test data DataFrame
            
        Returns:
            Dictionary with MAE and MAPE metrics
        """
        if len(test_df) == 0:
            return {"mae": 0.0, "mape": 0.0}
        
        # Make predictions on test set
        forecast = model.predict(test_df[['ds']])
        
        # Calculate MAE
        mae = np.mean(np.abs(test_df['y'].values - forecast['yhat'].values))
        
        # Calculate MAPE (excluding zeros in actual values)
        actual = test_df['y'].values
        predicted = forecast['yhat'].values
        
        # Filter out zeros to avoid division by zero
        non_zero_mask = actual != 0
        if non_zero_mask.sum() > 0:
            mape = np.mean(np.abs((actual[non_zero_mask] - predicted[non_zero_mask]) / actual[non_zero_mask])) * 100
        else:
            mape = 0.0
        
        return {
            "mae": float(mae),
            "mape": float(mape)
        }
    
    def generate_forecast(
        self,
        hospital_id: str,
        blood_group: str,
        component: str,
        days: int = 7
    ) -> Dict:
        """
        Generate forecast for specified hospital, blood group, and component.
        
        Args:
            hospital_id: Hospital ID
            blood_group: Blood group
            component: Component type
            days: Number of days to forecast (default 7)
            
        Returns:
            Dictionary with forecast results and metrics
        """
        # Get historical usage data
        usage_data = self.usage_repo.get_aggregated_daily(
            hospital_id=hospital_id,
            blood_group=blood_group,
            component=component,
            days=self.history_days
        )
        
        # Preprocess data
        end_date = date.today()
        start_date = end_date - timedelta(days=self.history_days)
        df = self.preprocess_data(usage_data, start_date, end_date)
        
        # Check if we have enough data
        if len(df) < 14:  # Need at least 2 weeks of data
            return {
                "error": "Insufficient historical data for forecasting",
                "min_required_days": 14,
                "available_days": len(df)
            }
        
        # Train-test split
        train_df, test_df = self.train_test_split(df)
        
        # Train model
        model = self.train_model(train_df)
        
        # Evaluate model
        metrics = self.evaluate_model(model, test_df)
        
        # Generate future forecast
        future_dates = model.make_future_dataframe(periods=days, freq='D')
        forecast = model.predict(future_dates)
        
        # Extract forecast for future dates only
        forecast_start_idx = len(df)
        future_forecast = forecast.iloc[forecast_start_idx:].copy()
        
        # Format forecast results
        forecast_points = []
        for _, row in future_forecast.iterrows():
            forecast_points.append({
                "date": row['ds'].date().isoformat(),
                "predicted": max(0, round(row['yhat'], 2)),  # Ensure non-negative
                "lower": max(0, round(row['yhat_lower'], 2)),
                "upper": max(0, round(row['yhat_upper'], 2))
            })
        
        return {
            "hospital_id": hospital_id,
            "blood_group": blood_group,
            "component": component,
            "forecast": forecast_points,
            "metrics": metrics,
            "generated_at": date.today().isoformat(),
            "history_days": self.history_days,
            "forecast_days": days
        }
    
    def generate_and_store_forecast(
        self,
        hospital_id: str,
        blood_group: str,
        component: str,
        days: int = 7
    ) -> Dict:
        """
        Generate forecast and store in database.
        
        Args:
            hospital_id: Hospital ID
            blood_group: Blood group
            component: Component type
            days: Number of days to forecast
            
        Returns:
            Forecast result dictionary
        """
        result = self.generate_forecast(hospital_id, blood_group, component, days)
        
        if "error" not in result:
            # Store forecast in database
            for point in result["forecast"]:
                self.forecast_repo.create({
                    "hospital_id": hospital_id,
                    "blood_group": blood_group,
                    "component": component,
                    "forecast_date": point["date"],
                    "predicted_units": point["predicted"],
                    "lower_bound": point["lower"],
                    "upper_bound": point["upper"]
                })
        
        return result
    
    def get_stored_forecast(
        self,
        hospital_id: str,
        blood_group: Optional[str] = None,
        component: Optional[str] = None,
        days: int = 7
    ) -> List[Dict]:
        """
        Get stored forecasts from database.
        
        Args:
            hospital_id: Hospital ID
            blood_group: Optional blood group filter
            component: Optional component filter
            days: Number of days to retrieve
            
        Returns:
            List of forecast records
        """
        start_date = date.today()
        end_date = start_date + timedelta(days=days)
        
        forecasts = self.forecast_repo.get_by_hospital(
            hospital_id=hospital_id,
            blood_group=blood_group,
            component=component,
            start_date=start_date,
            end_date=end_date
        )
        
        return forecasts
