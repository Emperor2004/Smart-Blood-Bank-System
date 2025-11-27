"""Application configuration management."""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = Field(
        default="postgresql://bloodbank:bloodbank123@localhost:5432/smart_blood_bank",
        alias="DATABASE_URL"
    )
    
    # Application
    environment: str = Field(default="development", alias="ENVIRONMENT")
    secret_key: str = Field(default="change-me-in-production", alias="SECRET_KEY")
    debug: bool = Field(default=True, alias="DEBUG")
    backend_port: int = Field(default=8000, alias="BACKEND_PORT")
    
    # JWT
    jwt_secret_key: str = Field(default="change-me-in-production", alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_access_token_expire_minutes: int = Field(default=30, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # CORS
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8501", alias="CORS_ORIGINS")
    
    # Forecasting
    forecast_horizon_days: int = Field(default=7, alias="FORECAST_HORIZON_DAYS")
    forecast_history_days: int = Field(default=180, alias="FORECAST_HISTORY_DAYS")
    forecast_confidence_interval: float = Field(default=0.95, alias="FORECAST_CONFIDENCE_INTERVAL")
    
    # Transfer Recommendations
    transfer_radius_km: float = Field(default=50.0, alias="TRANSFER_RADIUS_KM")
    transfer_surplus_threshold: int = Field(default=5, alias="TRANSFER_SURPLUS_THRESHOLD")
    transfer_weight_expiry: float = Field(default=0.6, alias="TRANSFER_WEIGHT_EXPIRY")
    transfer_weight_distance: float = Field(default=0.2, alias="TRANSFER_WEIGHT_DISTANCE")
    transfer_weight_surplus: float = Field(default=0.2, alias="TRANSFER_WEIGHT_SURPLUS")
    transfer_speed_kmh: float = Field(default=40.0, alias="TRANSFER_SPEED_KMH")
    
    # Expiry Risk
    expiry_risk_threshold_days: int = Field(default=3, alias="EXPIRY_RISK_THRESHOLD_DAYS")
    
    # Donor Eligibility
    donor_eligibility_days: int = Field(default=90, alias="DONOR_ELIGIBILITY_DAYS")
    
    # SMS Gateway
    sms_gateway_enabled: bool = Field(default=False, alias="SMS_GATEWAY_ENABLED")
    sms_gateway_api_key: Optional[str] = Field(default=None, alias="SMS_GATEWAY_API_KEY")
    twilio_account_sid: Optional[str] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, alias="TWILIO_PHONE_NUMBER")
    
    # Email
    email_enabled: bool = Field(default=False, alias="EMAIL_ENABLED")
    smtp_host: Optional[str] = Field(default="smtp.gmail.com", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, alias="SMTP_PORT")
    smtp_user: Optional[str] = Field(default=None, alias="SMTP_USER")
    smtp_password: Optional[str] = Field(default=None, alias="SMTP_PASSWORD")
    email_from: str = Field(default="noreply@bloodbank.gov.in", alias="EMAIL_FROM")
    
    # e-RaktKosh
    eraktkosh_api_enabled: bool = Field(default=False, alias="ERAKTKOSH_API_ENABLED")
    eraktkosh_api_url: Optional[str] = Field(default=None, alias="ERAKTKOSH_API_URL")
    eraktkosh_api_key: Optional[str] = Field(default=None, alias="ERAKTKOSH_API_KEY")
    
    # Background Jobs
    scheduler_enabled: bool = Field(default=True, alias="SCHEDULER_ENABLED")
    forecast_job_hour: int = Field(default=2, alias="FORECAST_JOB_HOUR")
    forecast_job_minute: int = Field(default=0, alias="FORECAST_JOB_MINUTE")
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_file: str = Field(default="logs/app.log", alias="LOG_FILE")
    
    # Encryption
    encryption_key: Optional[str] = Field(default=None, alias="ENCRYPTION_KEY")
    
    # Performance
    max_workers: int = Field(default=4, alias="MAX_WORKERS")
    connection_pool_size: int = Field(default=10, alias="CONNECTION_POOL_SIZE")
    connection_pool_max_overflow: int = Field(default=20, alias="CONNECTION_POOL_MAX_OVERFLOW")
    
    # Feature Flags
    enable_model_drift_monitoring: bool = Field(default=True, alias="ENABLE_MODEL_DRIFT_MONITORING")
    enable_audit_logging: bool = Field(default=True, alias="ENABLE_AUDIT_LOGGING")
    enable_geospatial_queries: bool = Field(default=True, alias="ENABLE_GEOSPATIAL_QUERIES")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
