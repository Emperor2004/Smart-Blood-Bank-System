#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    🚀 VERCEL DEPLOYMENT SCRIPT 🚀                            ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install Vercel CLI"
        exit 1
    fi
    echo "✅ Vercel CLI installed"
fi

# Check if logged in
echo ""
echo "📝 Checking Vercel login status..."
vercel whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Not logged in to Vercel"
    echo "Please run: vercel login"
    exit 1
fi
echo "✅ Logged in to Vercel"

# Go to frontend directory
cd frontend || exit 1

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo ""
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

# Build locally to test
echo ""
echo "🔨 Building frontend locally..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi
echo "✅ Build successful"

# Ask for backend URL
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Backend URL Configuration"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Options:"
echo "  1. Use localhost (for testing)"
echo "  2. Use Render backend (if deployed)"
echo "  3. Enter custom URL"
echo ""
read -p "Choose option (1-3): " option

case $option in
    1)
        BACKEND_URL="http://localhost:8000"
        ;;
    2)
        read -p "Enter Render backend URL: " BACKEND_URL
        ;;
    3)
        read -p "Enter backend URL: " BACKEND_URL
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

# Update .env.production
echo "VITE_API_URL=$BACKEND_URL" > .env.production
echo "✅ Backend URL set to: $BACKEND_URL"

# Deploy to Vercel
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Deploying to Vercel..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════════╗"
    echo "║                    ✅ DEPLOYMENT SUCCESSFUL ✅                               ║"
    echo "╚══════════════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Your frontend is now live on Vercel!"
    echo ""
    echo "Next steps:"
    echo "  1. Note your Vercel URL from above"
    echo "  2. Update backend CORS to include Vercel URL"
    echo "  3. Test your deployment"
    echo ""
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check the error messages above"
    exit 1
fi
