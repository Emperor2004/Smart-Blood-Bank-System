#!/bin/bash

echo "🛑 Stopping Smart Blood Bank System..."

# Kill backend
pkill -f "uvicorn app.main:app" 2>/dev/null && echo "✅ Backend stopped"

# Kill frontend
pkill -f "vite" 2>/dev/null && echo "✅ Frontend stopped"

# Stop database
docker-compose stop db 2>/dev/null && echo "✅ Database stopped"

echo "✅ All services stopped"
