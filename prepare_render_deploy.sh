#!/bin/bash

echo "🚀 Preparing Smart Blood Bank System for Render Deployment"
echo "=========================================================="

# Check if git is initialized
if [ ! -d .git ]; then
    echo "❌ Git repository not initialized"
    echo "Run: git init && git add . && git commit -m 'Initial commit'"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  You have uncommitted changes"
    echo "Commit them before deploying:"
    echo "  git add ."
    echo "  git commit -m 'Prepare for Render deployment'"
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No git remote 'origin' found"
    echo "Add your GitHub repository:"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    exit 1
fi

echo ""
echo "✅ Pre-deployment checks:"
echo "  - render.yaml exists: $([ -f render.yaml ] && echo '✓' || echo '✗')"
echo "  - Dockerfile.backend.render exists: $([ -f Dockerfile.backend.render ] && echo '✓' || echo '✗')"
echo "  - frontend/Dockerfile exists: $([ -f frontend/Dockerfile ] && echo '✓' || echo '✗')"
echo "  - backend/requirements.txt exists: $([ -f backend/requirements.txt ] && echo '✓' || echo '✗')"
echo ""

# Show git status
echo "📊 Git Status:"
git status --short

echo ""
echo "📝 Next Steps:"
echo "1. Commit any remaining changes:"
echo "   git add ."
echo "   git commit -m 'Ready for Render deployment'"
echo ""
echo "2. Push to GitHub:"
echo "   git push origin main"
echo ""
echo "3. Deploy on Render:"
echo "   - Go to https://dashboard.render.com/"
echo "   - Click 'New +' → 'Blueprint'"
echo "   - Connect your GitHub repository"
echo "   - Render will auto-detect render.yaml"
echo "   - Click 'Apply' to deploy all services"
echo ""
echo "4. After deployment:"
echo "   - Backend: https://smart-blood-bank-backend.onrender.com/health"
echo "   - Frontend: https://smart-blood-bank-frontend.onrender.com"
echo "   - API Docs: https://smart-blood-bank-backend.onrender.com/docs"
echo ""
echo "📖 Full guide: See RENDER_FULL_DEPLOYMENT.md"
