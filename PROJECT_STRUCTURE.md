# Project Structure

This document describes the complete directory structure and purpose of each component in the Smart Blood Bank system.

## Directory Tree

```
smart-blood-bank/
├── .kiro/                          # Kiro specifications
│   └── specs/
│       └── smart-blood-bank/
│           ├── requirements.md     # System requirements (EARS format)
│           ├── design.md          # Technical design document
│           └── tasks.md           # Implementation task list
│
├── backend/                        # Python backend application
│   ├── app/                       # Main application package
│   │   ├── api/                   # API endpoint handlers
│   │   ├── models/                # SQLAlchemy ORM models
│   │   ├── repositories/          # Data access layer (Repository pattern)
│   │   ├── services/              # Business logic services
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   └── main.py                # FastAPI application entry point
│   │
│   ├── alembic/                   # Database migrations
│   │   ├── versions/              # Migration scripts
│   │   ├── env.py                 # Alembic environment config
│   │   └── script.py.mako         # Migration template
│   │
│   ├── logs/                      # Application logs
│   ├── __init__.py
│   ├── alembic.ini                # Alembic configuration
│   ├── pytest.ini                 # Pytest configuration
│   └── requirements.txt           # Python dependencies
│
├── docker/                         # Docker configurations
│   ├── Dockerfile.backend         # Backend container image
│   └── init.sql                   # PostgreSQL initialization
│
├── frontend/                       # Frontend application (TBD)
│   └── (Streamlit or React app)
│
├── scripts/                        # Utility scripts
│   ├── check_setup.py             # Environment verification
│   └── init_db.py                 # Database initialization
│
├── tests/                          # Test suite
│   ├── __init__.py
│   └── test_setup.py              # Setup verification tests
│
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── docker-compose.yml              # Docker Compose configuration
├── Makefile                        # Common commands (Unix/Mac)
├── setup.bat                       # Setup script (Windows)
├── README.md                       # Main documentation
├── QUICKSTART.md                   # Quick start guide
└── PROJECT_STRUCTURE.md            # This file
```

## Component Descriptions

### Backend Application (`backend/app/`)

#### API Layer (`api/`)
- REST API endpoints using FastAPI
- Request/response validation with Pydantic
- Authentication and authorization middleware
- Will contain: `inventory.py`, `forecast.py`, `transfer.py`, `donor.py`, `auth.py`

#### Models Layer (`models/`)
- SQLAlchemy ORM models
- Database table definitions
- Relationships and constraints
- Will contain: `hospital.py`, `inventory.py`, `usage.py`, `donor.py`, `forecast.py`, `transfer.py`, `user.py`, `audit.py`

#### Repositories Layer (`repositories/`)
- Data access abstraction (Repository pattern)
- CRUD operations
- Complex queries
- Will contain: `hospital_repository.py`, `inventory_repository.py`, etc.

#### Services Layer (`services/`)
- Business logic implementation
- Orchestration of multiple repositories
- Algorithm implementations
- Will contain:
  - `ingestion_service.py` - CSV upload, validation, e-RaktKosh integration
  - `inventory_service.py` - Inventory management
  - `forecast_service.py` - ML-based demand forecasting
  - `expiry_service.py` - Expiry risk calculation
  - `transfer_service.py` - Transfer recommendations
  - `donor_service.py` - Donor management
  - `notification_service.py` - SMS/Email notifications
  - `auth_service.py` - Authentication and authorization

### Database Migrations (`backend/alembic/`)

- Version-controlled database schema changes
- Automatic migration generation with `alembic revision --autogenerate`
- Migration history in `versions/` directory

### Docker Configuration (`docker/`)

- **Dockerfile.backend**: Multi-stage build for production deployment
- **init.sql**: PostgreSQL initialization scripts
- **docker-compose.yml**: Local development environment with PostgreSQL

### Tests (`tests/`)

Test organization:
- `test_setup.py` - Environment verification
- `test_models.py` - Database model tests (Task 2)
- `test_services.py` - Business logic tests
- `test_api.py` - API endpoint tests
- `test_properties.py` - Property-based tests (Hypothesis)

### Scripts (`scripts/`)

Utility scripts for development and deployment:
- `check_setup.py` - Verify environment configuration
- `init_db.py` - Initialize database with migrations
- Future: `seed_data.py`, `backup_db.py`, `deploy.py`

## Configuration Files

### `.env.example`
Template for environment variables. Copy to `.env` and customize:
- Database connection
- API keys (SMS, e-RaktKosh)
- Feature flags
- Algorithm parameters

### `alembic.ini`
Alembic migration tool configuration:
- Database URL
- Migration script location
- Logging configuration

### `pytest.ini`
Test framework configuration:
- Test discovery patterns
- Coverage settings
- Test markers (unit, integration, property)

### `docker-compose.yml`
Multi-container application setup:
- PostgreSQL database service
- Backend API service
- Volume mounts for development
- Network configuration

### `requirements.txt`
Python dependencies:
- Web framework (FastAPI, Uvicorn)
- Database (SQLAlchemy, Alembic, psycopg2)
- ML (Prophet, Pandas, NumPy)
- Testing (pytest, Hypothesis)
- Utilities (Pydantic, python-dotenv)

## Development Workflow

1. **Setup**: Run `python scripts/check_setup.py`
2. **Database**: Start with `docker-compose up -d db`
3. **Migrations**: Apply with `alembic upgrade head`
4. **Development**: Run server with `uvicorn app.main:app --reload`
5. **Testing**: Run tests with `pytest tests/ -v`

## File Naming Conventions

- **Python files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Test files**: `test_*.py`
- **Migration files**: Auto-generated by Alembic

## Import Structure

```python
# Standard library
import os
from datetime import datetime

# Third-party
from fastapi import FastAPI
from sqlalchemy import Column

# Local application
from app.models import Hospital
from app.services import InventoryService
from app.config import settings
```

## Next Steps

1. Implement Task 2: Database schema and models
2. Create initial migration
3. Implement data ingestion layer
4. Build forecasting engine
5. Develop transfer recommendation system

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
