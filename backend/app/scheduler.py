"""Background job scheduler."""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.config import settings
from app.database import SessionLocal

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def generate_daily_forecasts():
    """Background job to generate daily forecasts for all hospitals."""
    from app.repositories.hospital import HospitalRepository
    from app.services.forecast import ForecastService
    from app.schemas.enums import BloodGroup, Component
    
    logger.info("Starting daily forecast generation job...")
    db = SessionLocal()
    
    try:
        hospital_repo = HospitalRepository(db)
        forecast_service = ForecastService(db)
        
        hospitals = hospital_repo.get_all()
        blood_groups = list(BloodGroup)
        components = list(Component)
        
        forecast_count = 0
        for hospital in hospitals:
            for blood_group in blood_groups:
                for component in components:
                    try:
                        forecast_service.generate_and_store_forecast(
                            hospital_id=hospital.hospital_id,
                            blood_group=blood_group.value,
                            component=component.value,
                            days=7
                        )
                        forecast_count += 1
                    except Exception as e:
                        logger.error(f"Failed to generate forecast for {hospital.hospital_id}, {blood_group.value}, {component.value}: {str(e)}")
        
        logger.info(f"Daily forecast generation completed. Generated {forecast_count} forecasts.")
        
    except Exception as e:
        logger.error(f"Error in daily forecast job: {str(e)}")
    finally:
        db.close()


def start_scheduler():
    """Start the background scheduler."""
    global scheduler
    
    if not settings.scheduler_enabled:
        logger.info("Scheduler is disabled in configuration")
        return
    
    if scheduler is not None:
        logger.warning("Scheduler already started")
        return
    
    scheduler = BackgroundScheduler()
    
    # Add daily forecast job
    scheduler.add_job(
        generate_daily_forecasts,
        CronTrigger(
            hour=settings.forecast_job_hour,
            minute=settings.forecast_job_minute
        ),
        id='daily_forecast_job',
        name='Generate daily forecasts',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info(f"Scheduler started. Daily forecast job scheduled at {settings.forecast_job_hour}:{settings.forecast_job_minute:02d}")


def stop_scheduler():
    """Stop the background scheduler."""
    global scheduler
    
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None
        logger.info("Scheduler stopped")
