# Backend Deployment Info

## 🌐 Public URL
```
https://yolande-nondivisional-norah.ngrok-free.dev
```

## 🔗 Quick Links

| Endpoint | URL |
|----------|-----|
| Health Check | https://yolande-nondivisional-norah.ngrok-free.dev/health |
| API Documentation | https://yolande-nondivisional-norah.ngrok-free.dev/docs |
| ReDoc | https://yolande-nondivisional-norah.ngrok-free.dev/redoc |
| Root | https://yolande-nondivisional-norah.ngrok-free.dev/ |

## 📊 Local Monitoring

| Service | URL |
|---------|-----|
| Backend (local) | http://localhost:8000 |
| ngrok Dashboard | http://localhost:4040 |
| ngrok Web Dashboard | https://dashboard.ngrok.com |

## 🛠️ Management

### View Logs
```bash
# Backend logs
tail -f backend.log

# ngrok logs
tail -f ngrok.log
```

### Stop Services
```bash
# Stop backend
pkill -f "uvicorn app.main:app"

# Stop ngrok
pkill ngrok

# Stop database
docker-compose down
```

### Restart Services
```bash
# Restart backend
./start_backend.sh

# Restart ngrok (will get new URL)
ngrok http 8000
```

## 🧪 Test Commands

```bash
# Health check
curl https://yolande-nondivisional-norah.ngrok-free.dev/health

# Root endpoint
curl https://yolande-nondivisional-norah.ngrok-free.dev/

# Test with frontend
# Update frontend .env:
# VITE_API_URL=https://yolande-nondivisional-norah.ngrok-free.dev
```

## ⚠️ Important

- **ngrok URL changes** when you restart ngrok (free tier)
- **Keep processes running** in background
- **CORS is configured** for this URL
- **Database is running** on localhost:5432

## 📱 For Frontend Integration

Use this in your frontend `.env`:
```env
VITE_API_URL=https://yolande-nondivisional-norah.ngrok-free.dev
```

Or in your API calls:
```javascript
const API_URL = 'https://yolande-nondivisional-norah.ngrok-free.dev';
```
