#!/bin/bash

echo "🩸 Smart Blood Bank Deployment Script"
echo "======================================"
echo ""

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok is not installed. Please install it from https://ngrok.com/download"
    exit 1
fi

# Check if database is running
echo "📊 Checking database..."
if ! docker ps | grep -q postgres; then
    echo "⚠️  PostgreSQL not running. Starting with Docker Compose..."
    docker-compose up -d db
    sleep 3
fi

# Run migrations
echo "🔄 Running database migrations..."
cd backend
source .venv/bin/activate
alembic upgrade head
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Start the backend server:"
echo "   ./start_backend.sh"
echo ""
echo "2. In a new terminal, start ngrok:"
echo "   ngrok http 8000"
echo ""
echo "3. Copy the ngrok HTTPS URL (e.g., https://abc123.ngrok.io)"
echo ""
echo "4. Update backend/.env CORS_ORIGINS with the ngrok URL"
echo ""
echo "5. Deploy frontend to Vercel:"
echo "   cd frontend"
echo "   vercel"
echo "   # Set VITE_API_URL to your ngrok URL"
echo ""
echo "📖 Full guide: NGROK_VERCEL_DEPLOYMENT.md"
