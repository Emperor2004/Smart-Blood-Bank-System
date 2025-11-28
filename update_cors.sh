#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./update_cors.sh <ngrok-url> [vercel-url]"
    echo "Example: ./update_cors.sh https://abc123.ngrok.io https://my-app.vercel.app"
    exit 1
fi

NGROK_URL=$1
VERCEL_URL=${2:-""}

if [ -z "$VERCEL_URL" ]; then
    NEW_CORS="http://localhost:3000,$NGROK_URL"
else
    NEW_CORS="http://localhost:3000,$NGROK_URL,$VERCEL_URL"
fi

# Update .env file
if [ -f .env ]; then
    if grep -q "^CORS_ORIGINS=" .env; then
        sed -i "s|^CORS_ORIGINS=.*|CORS_ORIGINS=$NEW_CORS|" .env
        echo "✅ Updated CORS_ORIGINS in .env"
        echo "   New value: $NEW_CORS"
    else
        echo "CORS_ORIGINS=$NEW_CORS" >> .env
        echo "✅ Added CORS_ORIGINS to .env"
    fi
else
    echo "❌ .env file not found"
    exit 1
fi

echo ""
echo "⚠️  Remember to restart the backend server for changes to take effect!"
