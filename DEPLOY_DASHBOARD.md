# Deploy via Render Dashboard

## 🚀 Quick Deploy (5 minutes)

Your code is already pushed to GitHub. Now deploy via Render Dashboard.

### Step 1: Go to Render Dashboard

Open: https://dashboard.render.com/

### Step 2: Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Fill in:
   - **Name**: `smart-blood-bank-db`
   - **Database**: `smart_blood_bank`
   - **User**: `bloodbank_user`
   - **Region**: Oregon (US West) - or closest to you
   - **Plan**: **Free**
3. Click **"Create Database"**
4. Wait 2-3 minutes for provisioning
5. **Copy the Internal Database URL** (you'll need this)

### Step 3: Deploy Backend

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Smart-Blood-Bank-System`
3. Fill in:
   - **Name**: `smart-blood-bank-backend`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Runtime**: **Docker**
   - **Dockerfile Path**: `Dockerfile.backend.render`
   - **Plan**: **Free**
4. Click **"Advanced"** and add environment variables:
   ```
   DATABASE_URL = <paste Internal Database URL from Step 2>
   ENVIRONMENT = production
   DEBUG = False
   SECRET_KEY = <click "Generate" button>
   JWT_SECRET_KEY = <click "Generate" button>
   LOG_LEVEL = INFO
   SCHEDULER_ENABLED = False
   CORS_ORIGINS = *
   ```
5. Click **"Create Web Service"**
6. Wait 5-7 minutes for build and deployment

### Step 4: Deploy Frontend

1. Click **"New +"** → **"Static Site"**
2. Connect your GitHub repository: `Smart-Blood-Bank-System`
3. Fill in:
   - **Name**: `smart-blood-bank-frontend`
   - **Branch**: `main`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
4. Add environment variable:
   ```
   VITE_API_URL = https://smart-blood-bank-backend.onrender.com
   ```
   (Replace with your actual backend URL from Step 3)
5. Click **"Create Static Site"**
6. Wait 3-5 minutes for build

### Step 5: Run Migrations

1. Go to backend service → **Shell** tab
2. Run:
   ```bash
   alembic upgrade head
   ```

### Step 6: Create Admin User

In the same shell:
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

## ✅ Done!

Your URLs:
- **Frontend**: https://smart-blood-bank-frontend.onrender.com
- **Backend**: https://smart-blood-bank-backend.onrender.com
- **API Docs**: https://smart-blood-bank-backend.onrender.com/docs

## 💰 Cost

- Database: FREE for 90 days, then $7/month
- Backend: FREE forever (sleeps after 15 min)
- Frontend: FREE forever (always on)

## 🐛 Troubleshooting

### Backend won't start
- Check logs in backend service
- Verify DATABASE_URL is correct (use Internal URL, not External)
- Check all environment variables are set

### Frontend can't reach backend
- Update VITE_API_URL with correct backend URL
- Redeploy frontend after changing env var

### Database connection failed
- Use **Internal Database URL** (not External)
- Format: `postgresql://user:pass@host/dbname`
