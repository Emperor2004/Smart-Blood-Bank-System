#!/bin/bash

echo "🚀 Starting Smart Blood Bank System Locally"
echo "==========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Start PostgreSQL
echo "📦 Starting PostgreSQL..."
docker-compose up -d db

echo "⏳ Waiting for database to be ready..."
sleep 5

# Check if backend venv exists
if [ ! -d "backend/.venv" ] && [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Virtual environment exists"
fi

# Run migrations
echo "🔧 Running database migrations..."
cd backend
source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
alembic upgrade head
cd ..

# Start backend
echo "🚀 Starting backend..."
cd backend
source .venv/bin/activate 2>/dev/null || source venv/bin/activate 2>/dev/null
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

echo "⏳ Waiting for backend to start..."
sleep 3

# Start frontend
echo "🚀 Starting frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ All services started!"
echo ""
echo "🔗 URLs:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo "   Database:  localhost:5432"
echo ""
echo "📊 Process IDs:"
echo "   Backend:  $BACKEND_PID"
echo "   Frontend: $FRONTEND_PID"
echo ""
echo "🛑 To stop all services:"
echo "   Press Ctrl+C or run: ./stop_local.sh"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker-compose stop db; echo '✅ Stopped'; exit" INT

wait
