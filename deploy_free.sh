#!/bin/bash

echo "🆓 Smart Blood Bank - 100% FREE Render Deployment"
echo "=================================================="
echo ""
echo "⚠️  IMPORTANT: Render does NOT offer free PostgreSQL"
echo "You need a free external database first!"
echo ""
echo "📋 Free Database Options:"
echo ""
echo "1. Neon (Recommended) - https://neon.tech"
echo "   ✓ 0.5 GB storage"
echo "   ✓ Always on"
echo "   ✓ Easy setup"
echo ""
echo "2. Supabase - https://supabase.com"
echo "   ✓ 500 MB database"
echo "   ✓ 2 GB bandwidth"
echo "   ✓ Pauses after 7 days idle"
echo ""
echo "3. ElephantSQL - https://elephantsql.com"
echo "   ✓ 20 MB storage (Tiny Turtle)"
echo "   ✓ Good for testing"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Have you created a free database? (y/n): " has_db

if [ "$has_db" != "y" ]; then
    echo ""
    echo "❌ Please create a free database first:"
    echo "   1. Go to https://neon.tech (recommended)"
    echo "   2. Sign up (free, no credit card)"
    echo "   3. Create project: 'smart-blood-bank'"
    echo "   4. Copy the connection string"
    echo "   5. Run this script again"
    exit 1
fi

echo ""
read -p "Enter your database connection string: " db_url

if [ -z "$db_url" ]; then
    echo "❌ Database URL required"
    exit 1
fi

echo ""
echo "✅ Configuration:"
echo "   Backend: Render Free (sleeps after 15 min)"
echo "   Frontend: Render Static (always on)"
echo "   Database: External (${db_url:0:30}...)"
echo ""
echo "💰 Total Cost: $0/month"
echo ""
read -p "Continue with deployment? (y/n): " confirm

if [ "$confirm" != "y" ]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Commit and push to GitHub:"
echo "   git add ."
echo "   git commit -m 'Deploy to Render - Free tier'"
echo "   git push origin main"
echo ""
echo "2. Deploy on Render:"
echo "   - Go to https://dashboard.render.com/"
echo "   - Click 'New +' → 'Blueprint'"
echo "   - Connect your GitHub repository"
echo "   - Click 'Apply'"
echo ""
echo "3. After deployment, set DATABASE_URL:"
echo "   - Go to Backend service → Environment"
echo "   - Set DATABASE_URL to: $db_url"
echo "   - Save (auto-redeploys)"
echo ""
echo "4. Run migrations in Backend Shell:"
echo "   alembic upgrade head"
echo ""
echo "5. Create admin user in Backend Shell:"
echo "   python -c \"from app.database import SessionLocal; from app.models import User; from passlib.context import CryptContext; db = SessionLocal(); pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto'); admin = User(username='admin', email='admin@hospital.gov.in', hashed_password=pwd_context.hash('admin123'), role='admin', is_active=True); db.add(admin); db.commit(); print('Admin created')\""
echo ""
echo "📖 Full guide: RENDER_FREE_DEPLOY.md"
echo ""
echo "🎉 Ready to deploy!"
