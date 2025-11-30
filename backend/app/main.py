"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Smart Blood Bank API",
    description="API for blood bank inventory management, forecasting, and transfer recommendations",
    version="1.0.0",
    debug=settings.debug
)

# Configure CORS
origins = settings.cors_origins.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Smart Blood Bank API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    from app.scheduler import start_scheduler
    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    from app.scheduler import stop_scheduler
    stop_scheduler()


# API routers
from app.api import inventory, hospital, dashboard, forecast, transfer, donor, notification, auth, eraktkosh

app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["inventory"])
app.include_router(hospital.router, prefix="/api/hospitals", tags=["hospitals"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["dashboard"])
app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])
app.include_router(transfer.router, prefix="/api/transfers", tags=["transfers"])
app.include_router(donor.router, prefix="/api/donors", tags=["donors"])
app.include_router(notification.router, prefix="/api/notifications", tags=["notifications"])

# Additional routers will be added in subsequent tasks
# from app.api import forecast, transfer, donor, auth
# app.include_router(forecast.router, prefix="/api/forecast", tags=["forecast"])
# app.include_router(transfer.router, prefix="/api/transfers", tags=["transfers"])
# app.include_router(donor.router, prefix="/api/donors", tags=["donors"])
# app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(eraktkosh.router, prefix="/api/eraktkosh", tags=["eraktkosh"])
