# Deploy to Render - Quick Reference

## 🚀 One-Command Deploy

```bash
./prepare_render_deploy.sh
```

## 📋 Manual Steps

### 1. Commit & Push
```bash
git add .
git commit -m "Deploy to Render"
git push origin main
```

### 2. Deploy on Render
1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repository
4. Select your repo
5. Click **"Apply"**

### 3. Wait for Deployment
- Database: ~2 minutes
- Backend: ~5 minutes (includes migrations)
- Frontend: ~3 minutes

### 4. Access Your App
- **Frontend**: https://smart-blood-bank-frontend.onrender.com
- **Backend API**: https://smart-blood-bank-backend.onrender.com/docs
- **Health Check**: https://smart-blood-bank-backend.onrender.com/health

## 🔧 What Gets Deployed

### Database (PostgreSQL)
- Name: `smart-blood-bank-db`
- Plan: Starter (free for 90 days)
- Internal access only

### Backend (FastAPI)
- Auto-connects to database
- Runs migrations on startup
- CORS configured for frontend
- Health check enabled

### Frontend (React + Nginx)
- Points to backend API
- Serves static files
- SPA routing enabled

## 🔐 Create Admin User

After backend deploys, go to backend **Shell** and run:

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
print('✅ Admin created: admin / admin123')
"
```

## ✅ Verify Deployment

```bash
# Check backend health
curl https://smart-blood-bank-backend.onrender.com/health

# Check frontend
curl https://smart-blood-bank-frontend.onrender.com

# Test API
curl https://smart-blood-bank-backend.onrender.com/api/hospitals
```

## 🐛 Troubleshooting

### Backend not starting?
- Check logs in Render dashboard
- Verify DATABASE_URL is set
- Look for migration errors

### Frontend can't reach backend?
- Check VITE_API_URL in frontend env vars
- Verify CORS_ORIGINS in backend
- Test backend health endpoint

### Database connection failed?
- Wait 2 minutes for DB to provision
- Check DATABASE_URL format
- Verify backend has DB access

## 💰 Cost
- **Free tier**: All services free (with sleep after 15min idle)
- **Starter tier**: $21/month total (always on)

## 📚 Full Documentation
See `RENDER_FULL_DEPLOYMENT.md` for complete guide.
