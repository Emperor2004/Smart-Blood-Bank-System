# Render Deployment Checklist

## Pre-Deployment ✓

- [ ] All code committed to git
- [ ] GitHub repository created and pushed
- [ ] Render account created
- [ ] GitHub connected to Render

## Files Ready ✓

- [ ] `render.yaml` - Blueprint configuration
- [ ] `Dockerfile.backend.render` - Backend Docker config
- [ ] `frontend/Dockerfile` - Frontend Docker config
- [ ] `frontend/nginx.conf.template` - Nginx config
- [ ] `backend/requirements.txt` - Python dependencies
- [ ] `backend/alembic/` - Database migrations

## Deployment Steps

### Step 1: Commit Changes
```bash
cd "/home/emperor/Projects/Smart Blood Bank System"
git add .
git commit -m "Deploy to Render with PostgreSQL"
git push origin main
```

### Step 2: Deploy on Render
1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Blueprint"**
3. Connect GitHub repository
4. Select repository: `Smart Blood Bank System`
5. Render detects `render.yaml`
6. Review services:
   - ✓ Database: smart-blood-bank-db
   - ✓ Backend: smart-blood-bank-backend
   - ✓ Frontend: smart-blood-bank-frontend
7. Click **"Apply"**

### Step 3: Monitor Deployment
- [ ] Database provisioning (2-3 min)
- [ ] Backend building (3-5 min)
- [ ] Backend migrations running
- [ ] Backend health check passing
- [ ] Frontend building (2-3 min)
- [ ] Frontend serving

### Step 4: Verify Services

#### Database
- [ ] Status: Available
- [ ] Connection string generated
- [ ] Linked to backend

#### Backend
- [ ] Status: Live
- [ ] Health check: https://smart-blood-bank-backend.onrender.com/health
- [ ] API docs: https://smart-blood-bank-backend.onrender.com/docs
- [ ] Logs show: "alembic upgrade head" success
- [ ] Logs show: "Application startup complete"

#### Frontend
- [ ] Status: Live
- [ ] URL loads: https://smart-blood-bank-frontend.onrender.com
- [ ] Can reach backend API
- [ ] No CORS errors in browser console

### Step 5: Create Admin User

Go to backend service → **Shell** tab:

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
print('Admin user created successfully')
"
```

- [ ] Admin user created
- [ ] Can login with: admin / admin123

### Step 6: Test Functionality

#### Authentication
- [ ] Login works
- [ ] JWT token received
- [ ] Protected routes accessible

#### Inventory Management
- [ ] Can view inventory
- [ ] Can add inventory manually
- [ ] Can upload CSV
- [ ] Can update inventory
- [ ] Can delete inventory

#### Hospital Management
- [ ] Can view hospitals
- [ ] Can add hospital
- [ ] Can update hospital

#### Dashboard
- [ ] Dashboard loads
- [ ] Statistics display
- [ ] Charts render

#### Forecasting
- [ ] Can generate forecast
- [ ] Prophet model runs
- [ ] Results display

#### Transfers
- [ ] Can view transfer recommendations
- [ ] Can create transfer request
- [ ] Can approve/reject transfer

#### Donors
- [ ] Can search donors
- [ ] Can add donor
- [ ] Can view donor history

## Post-Deployment

### Configuration
- [ ] Update CORS_ORIGINS if needed (backend env var)
- [ ] Configure SMS gateway (optional)
- [ ] Configure email notifications (optional)
- [ ] Set up custom domain (optional)

### Monitoring
- [ ] Check backend logs for errors
- [ ] Check frontend logs
- [ ] Monitor database size
- [ ] Test API response times

### Documentation
- [ ] Document admin credentials (securely)
- [ ] Document service URLs
- [ ] Share access with team
- [ ] Update project README with live URLs

## Troubleshooting

### Backend won't start
- [ ] Check logs for errors
- [ ] Verify DATABASE_URL is set
- [ ] Check migration logs
- [ ] Verify all env vars present

### Frontend can't reach backend
- [ ] Check VITE_API_URL is correct
- [ ] Verify backend is live
- [ ] Check CORS_ORIGINS in backend
- [ ] Test backend health endpoint

### Database connection errors
- [ ] Wait for DB to finish provisioning
- [ ] Check DATABASE_URL format
- [ ] Verify backend has DB access
- [ ] Check database status in dashboard

### Services sleeping (Free tier)
- [ ] First request takes ~30s
- [ ] Upgrade to Starter for always-on
- [ ] Or accept sleep behavior

## URLs Reference

### Production URLs
- **Frontend**: https://smart-blood-bank-frontend.onrender.com
- **Backend**: https://smart-blood-bank-backend.onrender.com
- **API Docs**: https://smart-blood-bank-backend.onrender.com/docs
- **Health**: https://smart-blood-bank-backend.onrender.com/health

### Render Dashboard
- **Services**: https://dashboard.render.com/
- **Database**: https://dashboard.render.com/databases
- **Logs**: Click service → Logs tab
- **Shell**: Click service → Shell tab

## Success Criteria

- [ ] All services show "Live" status
- [ ] Frontend loads without errors
- [ ] Can login as admin
- [ ] Can perform CRUD operations
- [ ] API responds within 500ms
- [ ] No errors in logs
- [ ] Database connected
- [ ] Migrations applied

## Next Steps

- [ ] Load sample data
- [ ] Configure notifications
- [ ] Set up monitoring alerts
- [ ] Plan for scaling
- [ ] Schedule regular backups
- [ ] Document operational procedures

## Support

If issues persist:
1. Check `RENDER_FULL_DEPLOYMENT.md` for detailed guide
2. Review `RENDER_ARCHITECTURE.md` for system overview
3. Check Render status: https://status.render.com
4. Contact Render support: support@render.com

---

**Deployment Date**: _________________

**Deployed By**: _________________

**Status**: ⬜ Success  ⬜ Issues  ⬜ Failed

**Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________
