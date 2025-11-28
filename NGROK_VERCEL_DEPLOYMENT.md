# Deployment Guide: Backend (ngrok) + Frontend (Vercel)

## Prerequisites

1. **ngrok account**: Sign up at https://ngrok.com
2. **Vercel account**: Sign up at https://vercel.com
3. **PostgreSQL database**: Running locally or on a cloud service

## Part 1: Deploy Backend to ngrok

### Step 1: Install ngrok

```bash
# Download and install ngrok
# Visit https://ngrok.com/download and follow instructions for your OS

# Or use snap on Linux
sudo snap install ngrok
```

### Step 2: Authenticate ngrok

```bash
# Get your auth token from https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 3: Start PostgreSQL Database

```bash
# Using Docker Compose
docker-compose up -d db

# Or start your local PostgreSQL
```

### Step 4: Run Database Migrations

```bash
cd backend
source .venv/bin/activate
alembic upgrade head
```

### Step 5: Start Backend Server

```bash
# From project root
./start_backend.sh

# Or manually:
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Step 6: Start ngrok Tunnel

Open a new terminal and run:

```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Copy the HTTPS URL** (e.g., `https://abc123.ngrok.io`) - you'll need it for the frontend.

### Step 7: Update CORS Settings

Update your `.env` file to allow the ngrok URL and Vercel domain:

```bash
CORS_ORIGINS=http://localhost:3000,https://abc123.ngrok.io,https://your-app.vercel.app
```

Restart the backend server after updating.

## Part 2: Deploy Frontend to Vercel

### Step 1: Install Vercel CLI (Optional)

```bash
npm install -g vercel
```

### Step 2: Update Frontend Environment Variable

Create `frontend/.env.production`:

```bash
VITE_API_URL=https://abc123.ngrok.io
```

Replace `abc123.ngrok.io` with your actual ngrok URL.

### Step 3: Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
cd frontend
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? smart-blood-bank
# - Directory? ./
# - Override settings? No

# Set environment variable
vercel env add VITE_API_URL production
# Enter your ngrok URL: https://abc123.ngrok.io

# Deploy to production
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/new
2. Import your Git repository (GitHub/GitLab/Bitbucket)
3. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Add Environment Variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://abc123.ngrok.io` (your ngrok URL)
5. Click **Deploy**

### Step 4: Update Backend CORS

Once deployed, update your backend `.env` with the Vercel URL:

```bash
CORS_ORIGINS=http://localhost:3000,https://abc123.ngrok.io,https://your-app.vercel.app
```

Restart the backend server.

## Testing the Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try uploading a CSV file
3. Check the forecast functionality
4. Monitor ngrok dashboard: https://dashboard.ngrok.com

## Important Notes

### ngrok Free Tier Limitations
- URL changes every time you restart ngrok
- 40 connections/minute limit
- Session expires after 2 hours

### For Production Use

Consider these alternatives to ngrok:

1. **Backend Hosting**:
   - Render.com (free tier available)
   - Railway.app (free tier available)
   - Heroku (paid)
   - AWS EC2/ECS
   - Google Cloud Run

2. **Database**:
   - Render PostgreSQL (free tier)
   - Supabase (free tier)
   - AWS RDS
   - Neon.tech (free tier)

## Keeping ngrok URL Persistent

For a static ngrok URL (paid feature):

```bash
ngrok http 8000 --domain=your-static-domain.ngrok.io
```

## Troubleshooting

### Backend not accessible via ngrok
- Check if backend is running on port 8000
- Verify ngrok is forwarding to correct port
- Check firewall settings

### CORS errors
- Ensure backend CORS_ORIGINS includes both ngrok and Vercel URLs
- Restart backend after updating .env

### Frontend can't connect to backend
- Verify VITE_API_URL is set correctly in Vercel
- Check browser console for errors
- Verify ngrok tunnel is active

### Database connection issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in backend .env
- Verify database migrations are applied

## Monitoring

- **ngrok Dashboard**: https://dashboard.ngrok.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **Backend Logs**: Check terminal where backend is running
- **Frontend Logs**: Check Vercel deployment logs

## Stopping Services

```bash
# Stop backend: Ctrl+C in backend terminal
# Stop ngrok: Ctrl+C in ngrok terminal
# Stop database: docker-compose down
```
