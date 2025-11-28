# Deployment Status

**Deployed on:** 2025-11-28 13:49 IST

## Services Running

### ✅ Database (PostgreSQL 14)
- **Container:** blood_bank_db
- **Status:** Running & Healthy
- **Port:** 5432
- **Connection:** `postgresql://bloodbank:bloodbank123@localhost:5432/smart_blood_bank`

### ✅ Backend (FastAPI + Gunicorn)
- **Container:** blood_bank_backend
- **Status:** Running (2 workers)
- **Port:** 8000
- **Health Check:** http://localhost:8000/health
- **API Documentation:** http://localhost:8000/docs
- **Database Connection:** ✅ Verified

### ✅ Frontend (React + Vite + Nginx)
- **Container:** blood_bank_frontend
- **Status:** Running
- **Port:** 3000
- **URL:** http://localhost:3000
- **API Endpoint:** http://localhost:8000

## Connectivity Verified

- ✅ Frontend → Backend: Configured via `VITE_API_URL`
- ✅ Backend → Database: Connection pool active
- ✅ All health checks passing

## Quick Commands

```bash
# View logs
docker compose logs -f

# Stop services
docker compose down

# Restart services
docker compose restart

# Rebuild and restart
docker compose up -d --build

# Check status
docker compose ps
```

## Access Points

- **Frontend UI:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
