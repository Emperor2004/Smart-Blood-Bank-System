# Complete Render Deployment Guide

This guide walks you through deploying the Smart Blood Bank System on Render with PostgreSQL database, backend API, and frontend - all properly connected.

## Prerequisites

- GitHub account with your repository pushed
- Render account (free tier works)
- Git repository with all code committed

## Deployment Steps

### Step 1: Push Code to GitHub

```bash
# Ensure all changes are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Deploy Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Select the repository: `Smart Blood Bank System`
5. Render will detect `render.yaml` and show:
   - **Database**: smart-blood-bank-db (PostgreSQL)
   - **Backend**: smart-blood-bank-backend (Web Service)
   - **Frontend**: smart-blood-bank-frontend (Web Service)
6. Click **"Apply"**

Render will automatically:
- Create the PostgreSQL database
- Deploy the backend with DATABASE_URL connected
- Deploy the frontend with VITE_API_URL pointing to backend
- Run database migrations on backend startup

### Step 3: Verify Deployment

**Backend:**
- URL: `https://smart-blood-bank-backend.onrender.com`
- Health check: `https://smart-blood-bank-backend.onrender.com/health`
- API docs: `https://smart-blood-bank-backend.onrender.com/docs`

**Frontend:**
- URL: `https://smart-blood-bank-frontend.onrender.com`

**Database:**
- Connection string available in backend environment variables
- Accessible only by backend service (internal network)

### Step 4: Update Frontend URL (if needed)

If your backend URL is different from `smart-blood-bank-backend.onrender.com`:

1. Go to Frontend service settings
2. Update `VITE_API_URL` environment variable
3. Trigger manual deploy or redeploy

### Step 5: Create Initial Admin User

Once backend is deployed, create an admin user via the backend shell:

1. Go to backend service → **Shell** tab
2. Run:
```bash
python -c "
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext

db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

admin = User(
    username='admin',
    email='admin@hospital.gov.in',
    hashed_password=pwd_context.hash('admin123'),
    role='admin',
    is_active=True
)
db.add(admin)
db.commit()
print('Admin user created: admin / admin123')
"
```

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  Frontend (Nginx + React)                      │
│  https://smart-blood-bank-frontend.onrender.com│
└────────────────┬────────────────────────────────┘
                 │ HTTPS
                 │ VITE_API_URL
                 ▼
┌─────────────────────────────────────────────────┐
│  Backend (FastAPI + Gunicorn)                  │
│  https://smart-blood-bank-backend.onrender.com │
│  - CORS: allows frontend origin                │
│  - Health check: /health                       │
│  - API docs: /docs                             │
└────────────────┬────────────────────────────────┘
                 │ DATABASE_URL
                 │ (internal network)
                 ▼
┌─────────────────────────────────────────────────┐
│  PostgreSQL Database                           │
│  smart-blood-bank-db                           │
│  - Internal only (not publicly accessible)     │
│  - Auto-connected via render.yaml              │
└─────────────────────────────────────────────────┘
```

## Environment Variables

### Backend
- `DATABASE_URL`: Auto-injected from database
- `SECRET_KEY`: Auto-generated
- `JWT_SECRET_KEY`: Auto-generated
- `CORS_ORIGINS`: Set to "*" (or specific frontend URL)
- `ENVIRONMENT`: production
- `DEBUG`: False
- `LOG_LEVEL`: INFO
- `SCHEDULER_ENABLED`: True

### Frontend
- `VITE_API_URL`: Backend URL (https://smart-blood-bank-backend.onrender.com)

## Troubleshooting

### Backend won't start
- Check logs: Backend service → **Logs** tab
- Verify DATABASE_URL is set
- Ensure migrations ran: Look for "alembic upgrade head" in logs

### Frontend can't connect to backend
- Verify VITE_API_URL is correct
- Check backend CORS_ORIGINS includes frontend URL
- Test backend health: `curl https://smart-blood-bank-backend.onrender.com/health`

### Database connection errors
- Database takes ~2 minutes to provision on first deploy
- Backend waits for DB before starting (see Dockerfile CMD)
- Check database status in Render dashboard

### Services sleeping (Free tier)
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep takes ~30 seconds to wake up
- Upgrade to paid plan for always-on services

## Manual Deployment (Alternative)

If you prefer manual setup instead of render.yaml:

### 1. Create Database
- New → PostgreSQL
- Name: `smart-blood-bank-db`
- Plan: Starter (free)

### 2. Create Backend Service
- New → Web Service
- Connect repository
- Name: `smart-blood-bank-backend`
- Runtime: Docker
- Dockerfile path: `Dockerfile.backend.render`
- Plan: Starter (free)
- Add environment variables (see above)
- Link DATABASE_URL from database

### 3. Create Frontend Service
- New → Web Service
- Connect repository
- Name: `smart-blood-bank-frontend`
- Runtime: Docker
- Dockerfile path: `frontend/Dockerfile`
- Plan: Starter (free)
- Set VITE_API_URL to backend URL

## Cost Estimate

**Free Tier:**
- PostgreSQL: 90 days free, then $7/month
- Backend: Free (with sleep)
- Frontend: Free (with sleep)

**Starter Tier (Recommended):**
- PostgreSQL: $7/month
- Backend: $7/month (always on)
- Frontend: $7/month (always on)
- **Total: $21/month**

## Next Steps

1. Test all functionality via frontend
2. Upload sample inventory data
3. Configure SMS/email notifications (optional)
4. Set up custom domain (optional)
5. Enable automatic deployments on git push

## Support

- Render Docs: https://render.com/docs
- Project Issues: GitHub repository issues
- Render Community: https://community.render.com
