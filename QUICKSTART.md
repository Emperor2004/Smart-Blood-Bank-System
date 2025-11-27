# Quick Start Guide

Get the Smart Blood Bank system up and running in minutes.

## Prerequisites

- Python 3.10 or higher
- Docker Desktop (for PostgreSQL)
- Git

## Step-by-Step Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

Or on Windows, run:
```cmd
setup.bat
# Choose option 1
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (optional for local development)
```

The default settings in `.env.example` work for local development.

### 3. Start PostgreSQL Database

```bash
docker-compose up -d db
```

This starts PostgreSQL on port 5432 with the following credentials:
- Username: `bloodbank`
- Password: `bloodbank123`
- Database: `smart_blood_bank`

### 4. Verify Setup

```bash
python scripts/check_setup.py
```

This checks:
- Python version
- Installed dependencies
- Environment configuration
- Directory structure

### 5. Run Database Migrations

```bash
cd backend
alembic upgrade head
cd ..
```

Note: Initial migration will be created in Task 2.1

### 6. Start the Development Server

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or on Windows:
```cmd
setup.bat
# Choose option 8
```

### 7. Access the Application

- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Testing the Setup

```bash
cd backend
pytest ../tests/test_setup.py -v
```

## Common Issues

### Port 5432 Already in Use

If you have PostgreSQL already running locally:
1. Stop your local PostgreSQL service
2. Or change the port in `.env`: `DB_PORT=5433`
3. Update `docker-compose.yml` to use the new port

### Import Errors

Make sure you're in the correct directory when running commands:
- For running the server: `cd backend`
- For running scripts: run from project root

### Docker Issues

If Docker commands fail:
1. Ensure Docker Desktop is running
2. Check Docker daemon status: `docker ps`
3. Restart Docker Desktop if needed

## Next Steps

1. Review the [README.md](README.md) for detailed documentation
2. Check the task list: `.kiro/specs/smart-blood-bank/tasks.md`
3. Review the design document: `.kiro/specs/smart-blood-bank/design.md`
4. Start implementing Task 2: Database schema and models

## Useful Commands

```bash
# Check environment setup
python scripts/check_setup.py

# Start database
docker-compose up -d db

# Stop database
docker-compose down

# View database logs
docker-compose logs -f db

# Run migrations
cd backend && alembic upgrade head

# Create new migration
cd backend && alembic revision --autogenerate -m "description"

# Run tests
cd backend && pytest ../tests/ -v

# Run specific test
cd backend && pytest ../tests/test_setup.py -v

# Start server
cd backend && uvicorn app.main:app --reload

# Check API docs
# Open browser: http://localhost:8000/docs
```

## Development Workflow

1. Create a feature branch
2. Implement the task from `tasks.md`
3. Write tests (unit + property-based)
4. Run tests: `pytest`
5. Commit changes
6. Move to next task

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review the design document
- Check existing tests for examples
