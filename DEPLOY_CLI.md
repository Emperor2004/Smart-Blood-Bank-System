# Deploy with Render CLI - Quick Guide

## 💰 Cost
- Database: **Free for 90 days**, then **$7/month**
- Backend: **Free** (sleeps after 15 min)
- Frontend: **Free** (always on)

## 🚀 One-Command Deploy

```bash
./deploy_render_cli.sh
```

## 📦 Manual Steps

### 1. Install Render CLI

```bash
npm install -g @render/cli
```

### 2. Login

```bash
render login
```

### 3. Deploy

```bash
render blueprint launch
```

That's it! The `render.yaml` handles everything:
- Creates PostgreSQL database
- Deploys backend (auto-connects to DB)
- Deploys frontend
- Runs migrations on startup

## ✅ Verify

```bash
# Check services
render services list

# View backend logs
render service logs smart-blood-bank-backend --tail

# Get URLs
render service url smart-blood-bank-backend
render service url smart-blood-bank-frontend
```

## 🔧 Create Admin User

```bash
render service shell smart-blood-bank-backend

# In shell:
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
print('Admin created: admin / admin123')
"
```

## 🔗 Your URLs

- **Frontend**: https://smart-blood-bank-frontend.onrender.com
- **Backend**: https://smart-blood-bank-backend.onrender.com
- **API Docs**: https://smart-blood-bank-backend.onrender.com/docs

## 📊 Useful Commands

```bash
# View logs (live)
render service logs smart-blood-bank-backend --tail

# Restart service
render service restart smart-blood-bank-backend

# Open shell
render service shell smart-blood-bank-backend

# Check status
render service status smart-blood-bank-backend

# List all services
render services list

# Update env var
render service env set smart-blood-bank-backend KEY=value
```

## 🔄 Update Deployment

Just push to GitHub:
```bash
git push origin main
```

Auto-deploys on every push!

## 📖 Full Guide

See `RENDER_CLI_DEPLOY.md` for complete documentation.
