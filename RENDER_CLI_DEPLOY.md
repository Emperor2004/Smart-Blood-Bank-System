# Deploy with Render CLI

## 💰 Cost Warning

- **Database**: Free for 90 days, then **$7/month**
- **Backend**: Free (sleeps after 15 min)
- **Frontend**: Free (always on)

## 📦 Install Render CLI

```bash
# Install via npm
npm install -g @render/cli

# Or via pip
pip install render

# Verify installation
render --version
```

## 🔐 Login to Render

```bash
render login
```

This will open your browser to authenticate.

## 🚀 Deploy Everything

### Option 1: Deploy from render.yaml (Recommended)

```bash
# From project root
cd "/home/emperor/Projects/Smart Blood Bank System"

# Deploy all services (database + backend + frontend)
render blueprint launch
```

This will:
1. Create PostgreSQL database (free for 90 days)
2. Deploy backend with auto-connected DATABASE_URL
3. Deploy frontend static site
4. Run migrations automatically

### Option 2: Manual CLI Commands

```bash
# 1. Create database
render postgres create smart-blood-bank-db \
  --name smart_blood_bank \
  --plan free

# 2. Create backend service
render service create web smart-blood-bank-backend \
  --runtime docker \
  --dockerfilePath Dockerfile.backend.render \
  --plan free \
  --branch main

# 3. Link database to backend
render service env set smart-blood-bank-backend \
  DATABASE_URL=$(render postgres connection-string smart-blood-bank-db)

# 4. Create frontend static site
render service create static smart-blood-bank-frontend \
  --buildCommand "cd frontend && npm install && npm run build" \
  --publishPath frontend/dist \
  --branch main
```

## ✅ Verify Deployment

```bash
# List all services
render services list

# Check backend status
render service logs smart-blood-bank-backend

# Check frontend status
render service logs smart-blood-bank-frontend

# Check database status
render postgres list
```

## 🔧 Post-Deployment Setup

### 1. Run Migrations

```bash
# Open backend shell
render service shell smart-blood-bank-backend

# In the shell, run:
alembic upgrade head
exit
```

### 2. Create Admin User

```bash
# Open backend shell
render service shell smart-blood-bank-backend

# Create admin
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
exit
```

## 🔗 Get Service URLs

```bash
# Get backend URL
render service url smart-blood-bank-backend

# Get frontend URL
render service url smart-blood-bank-frontend
```

## 📊 Monitor Services

```bash
# View backend logs (live)
render service logs smart-blood-bank-backend --tail

# View frontend logs
render service logs smart-blood-bank-frontend --tail

# View database logs
render postgres logs smart-blood-bank-db
```

## 🔄 Update Deployment

```bash
# Trigger manual deploy
render service deploy smart-blood-bank-backend

# Or just push to GitHub (auto-deploys)
git push origin main
```

## 🗑️ Delete Services (if needed)

```bash
# Delete frontend
render service delete smart-blood-bank-frontend

# Delete backend
render service delete smart-blood-bank-backend

# Delete database (WARNING: deletes all data)
render postgres delete smart-blood-bank-db
```

## 🐛 Troubleshooting

### Check service status
```bash
render service status smart-blood-bank-backend
```

### View environment variables
```bash
render service env list smart-blood-bank-backend
```

### Update environment variable
```bash
render service env set smart-blood-bank-backend CORS_ORIGINS="*"
```

### Restart service
```bash
render service restart smart-blood-bank-backend
```

## 📖 Render CLI Reference

```bash
# Help
render --help

# Service commands
render service --help

# Database commands
render postgres --help

# Blueprint commands
render blueprint --help
```

## ⚡ Quick Commands

```bash
# Deploy everything
render blueprint launch

# View all services
render services list

# Backend logs
render service logs smart-blood-bank-backend --tail

# Backend shell
render service shell smart-blood-bank-backend

# Restart backend
render service restart smart-blood-bank-backend
```

## 🎯 Complete Deployment Script

Save as `deploy_render_cli.sh`:

```bash
#!/bin/bash
set -e

echo "🚀 Deploying to Render via CLI..."

# Check if logged in
if ! render whoami &>/dev/null; then
    echo "Please login first: render login"
    exit 1
fi

# Deploy from blueprint
echo "📦 Deploying services..."
render blueprint launch

echo "⏳ Waiting for services to be ready..."
sleep 30

# Get backend service name
BACKEND_SERVICE="smart-blood-bank-backend"

echo "🔧 Running migrations..."
render service shell $BACKEND_SERVICE -c "alembic upgrade head"

echo "👤 Creating admin user..."
render service shell $BACKEND_SERVICE -c "python -c \"
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
admin = User(username='admin', email='admin@hospital.gov.in', hashed_password=pwd_context.hash('admin123'), role='admin', is_active=True)
db.add(admin)
db.commit()
print('Admin created')
\""

echo "✅ Deployment complete!"
echo ""
echo "🔗 URLs:"
render service url smart-blood-bank-backend
render service url smart-blood-bank-frontend
```

## 💡 Tips

1. **Use blueprint**: `render blueprint launch` is easiest
2. **Monitor logs**: Use `--tail` flag for live logs
3. **Shell access**: Use `render service shell` for debugging
4. **Auto-deploy**: Push to GitHub triggers deployment
5. **Environment vars**: Manage via CLI or dashboard

## 📚 Documentation

- Render CLI: https://render.com/docs/cli
- Blueprint spec: https://render.com/docs/blueprint-spec
- PostgreSQL: https://render.com/docs/databases
