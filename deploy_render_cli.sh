#!/bin/bash
set -e

echo "🚀 Render CLI Deployment"
echo "========================"
echo ""
echo "💰 Cost: Database free for 90 days, then \$7/month"
echo "    Backend & Frontend: Free forever"
echo ""

# Check if Render CLI is installed
if ! command -v render &> /dev/null; then
    echo "❌ Render CLI not found"
    echo ""
    echo "Install it:"
    echo "  npm install -g @render/cli"
    echo "  # or"
    echo "  pip install render"
    exit 1
fi

echo "✅ Render CLI found: $(render --version)"
echo ""

# Check if logged in
if ! render whoami &>/dev/null; then
    echo "🔐 Please login to Render:"
    render login
fi

echo "✅ Logged in as: $(render whoami)"
echo ""

# Commit check
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "⚠️  Uncommitted changes detected"
    read -p "Commit changes now? (y/n): " commit_now
    if [ "$commit_now" = "y" ]; then
        git add .
        git commit -m "Deploy to Render via CLI"
    fi
fi

# Push check
echo "📤 Pushing to GitHub..."
git push origin main || echo "⚠️  Push failed or already up to date"
echo ""

# Deploy
echo "🚀 Deploying services from render.yaml..."
echo ""
render blueprint launch

echo ""
echo "⏳ Waiting for services to initialize (30s)..."
sleep 30

echo ""
echo "🔧 Running database migrations..."
render service shell smart-blood-bank-backend -c "alembic upgrade head" || echo "⚠️  Migration may need manual run"

echo ""
echo "👤 Creating admin user..."
render service shell smart-blood-bank-backend -c "python -c \"
from app.database import SessionLocal
from app.models import User
from passlib.context import CryptContext
db = SessionLocal()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
admin = User(username='admin', email='admin@hospital.gov.in', hashed_password=pwd_context.hash('admin123'), role='admin', is_active=True)
db.add(admin)
db.commit()
print('✅ Admin created: admin / admin123')
\"" || echo "⚠️  Admin creation may need manual run"

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "🔗 Your URLs:"
echo "   Backend:  $(render service url smart-blood-bank-backend 2>/dev/null || echo 'https://smart-blood-bank-backend.onrender.com')"
echo "   Frontend: $(render service url smart-blood-bank-frontend 2>/dev/null || echo 'https://smart-blood-bank-frontend.onrender.com')"
echo "   API Docs: $(render service url smart-blood-bank-backend 2>/dev/null || echo 'https://smart-blood-bank-backend.onrender.com')/docs"
echo ""
echo "📊 Monitor:"
echo "   render service logs smart-blood-bank-backend --tail"
echo "   render service logs smart-blood-bank-frontend --tail"
echo ""
echo "🎉 Done!"
