#!/bin/bash

echo "🩸 Smart Blood Bank - Deployment Setup"
echo "======================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install it first."
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install it first."
    exit 1
fi

# Check ngrok
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed."
    echo "   Install from: https://ngrok.com/download"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Install Vercel CLI
echo "📦 Installing Vercel CLI..."
npm install -g vercel

if [ $? -eq 0 ]; then
    echo "✅ Vercel CLI installed successfully"
else
    echo "⚠️  Vercel CLI installation failed. You can install it manually:"
    echo "   npm install -g vercel"
fi

echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Authenticate with ngrok (if not done):"
echo "   ngrok config add-authtoken YOUR_TOKEN"
echo "   Get token from: https://dashboard.ngrok.com/get-started/your-authtoken"
echo ""
echo "2. Authenticate with Vercel:"
echo "   vercel login"
echo ""
echo "3. Run the deployment:"
echo "   ./deploy.sh"
echo ""
echo "📖 Quick guide: QUICK_DEPLOY.md"
echo "📖 Full guide: NGROK_VERCEL_DEPLOYMENT.md"
