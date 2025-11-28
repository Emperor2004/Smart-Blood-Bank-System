# Vercel + Ngrok Deployment Guide

## Current Setup

**Backend (Ngrok):** https://yolande-nondivisional-norah.ngrok-free.dev
**Frontend (Vercel):** https://smart-blood-bank-system.vercel.app

## Steps to Connect Frontend to Backend

### 1. Frontend Environment Variable

In your Vercel project settings:

1. Go to **Settings** → **Environment Variables**
2. Add variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://yolande-nondivisional-norah.ngrok-free.dev`
   - **Environment:** Production

### 2. Redeploy Frontend

After adding the environment variable, trigger a new deployment:

```bash
cd frontend
git add .
git commit -m "Update API URL"
git push
```

Or use Vercel CLI:

```bash
cd frontend
vercel --prod
```

### 3. Backend CORS Configuration

The backend is already configured to allow:
- `http://localhost:3000`
- `https://smart-blood-bank-system.vercel.app`

CORS is now active in the running container.

## Testing the Connection

1. Open browser console on Vercel site
2. Check Network tab for API calls
3. Verify requests go to ngrok URL
4. Check for CORS errors (should be none)

## Troubleshooting

### If frontend can't reach backend:

1. **Check ngrok is running:**
   ```bash
   curl http://localhost:4040/api/tunnels
   ```

2. **Test backend directly:**
   ```bash
   curl https://yolande-nondivisional-norah.ngrok-free.dev/health
   ```

3. **Verify Vercel environment variable:**
   - Check Vercel dashboard → Settings → Environment Variables
   - Ensure `VITE_API_URL` is set correctly

4. **Check browser console:**
   - Look for CORS errors
   - Verify API URL in network requests

### If CORS errors occur:

Update `.env` file and restart backend:
```bash
# Add your Vercel URL to CORS_ORIGINS in .env
CORS_ORIGINS=http://localhost:3000,https://smart-blood-bank-system.vercel.app,https://your-new-url.vercel.app

# Restart backend
docker compose down
docker compose up -d
```

## Important Notes

- Ngrok free tier URLs change on restart
- Update `VITE_API_URL` in Vercel when ngrok URL changes
- Backend must be running for frontend to work
- CORS must include your Vercel deployment URL
