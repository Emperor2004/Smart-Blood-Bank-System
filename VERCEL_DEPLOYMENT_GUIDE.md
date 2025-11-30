# 🚀 Vercel Deployment Guide

## ⚠️ IMPORTANT: Vercel Limitations

**Vercel can only host the frontend (React app).**

For a complete deployment, you need:
1. **Frontend → Vercel** (Static React app)
2. **Backend → Render/Railway/Heroku** (FastAPI server)
3. **Database → Render/Railway/Neon** (PostgreSQL)

---

## 📋 DEPLOYMENT STRATEGY

### Option 1: Frontend Only on Vercel (Quick)
- Deploy frontend to Vercel
- Keep backend running locally
- Update frontend to point to local backend

### Option 2: Full Stack (Recommended)
- Deploy frontend to Vercel
- Deploy backend to Render (free tier)
- Deploy database to Render (free tier)
- Connect all services

---

## 🎯 OPTION 1: FRONTEND ONLY (5 MINUTES)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy Frontend

```bash
cd frontend
vercel
```

Follow prompts:
- Set up and deploy? **Y**
- Which scope? **Your account**
- Link to existing project? **N**
- Project name? **smart-blood-bank**
- Directory? **./frontend**
- Override settings? **N**

### Step 4: Set Environment Variable

After deployment, set the backend URL:

```bash
vercel env add VITE_API_URL
```

Enter value: `http://localhost:8000` (or your backend URL)

### Step 5: Redeploy

```bash
vercel --prod
```

**Done!** Frontend is live on Vercel.

---

## 🎯 OPTION 2: FULL STACK DEPLOYMENT

### Part A: Deploy Backend to Render

#### 1. Create Render Account
- Go to https://render.com
- Sign up (free)

#### 2. Create PostgreSQL Database
- Click "New +"
- Select "PostgreSQL"
- Name: `smart-blood-bank-db`
- Database: `smart_blood_bank`
- User: `bloodbank`
- Region: Choose closest
- Plan: **Free**
- Click "Create Database"

**Save the connection details:**
- Internal Database URL
- External Database URL

#### 3. Create Web Service for Backend
- Click "New +"
- Select "Web Service"
- Connect your GitHub repo (or use manual deploy)
- Name: `smart-blood-bank-api`
- Environment: **Python 3**
- Build Command: `pip install -r backend/requirements.txt`
- Start Command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Plan: **Free**

#### 4. Add Environment Variables on Render

```
DATABASE_URL=<your_render_postgres_url>
SECRET_KEY=<generate_random_32_chars>
JWT_SECRET_KEY=<generate_random_32_chars>
ENCRYPTION_KEY=<generate_random_32_chars>
CORS_ORIGINS=https://your-vercel-app.vercel.app
ENVIRONMENT=production
DEBUG=False
```

Generate keys:
```bash
openssl rand -hex 32
```

#### 5. Deploy Backend
- Click "Create Web Service"
- Wait for deployment (5-10 minutes)
- Note your backend URL: `https://smart-blood-bank-api.onrender.com`

### Part B: Deploy Frontend to Vercel

#### 1. Update Frontend Environment

Edit `frontend/.env.production`:
```bash
VITE_API_URL=https://smart-blood-bank-api.onrender.com
```

#### 2. Deploy to Vercel

```bash
cd frontend
vercel --prod
```

#### 3. Update Backend CORS

Go back to Render dashboard:
- Open your backend service
- Environment variables
- Update `CORS_ORIGINS` to include your Vercel URL:
  ```
  CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
  ```

**Done!** Full stack is live.

---

## 🚀 QUICK DEPLOY COMMANDS

### Frontend to Vercel (Current Directory)

```bash
# From project root
cd frontend

# Login (first time only)
vercel login

# Deploy
vercel --prod

# Set environment variable
vercel env add VITE_API_URL production
# Enter: https://your-backend-url.onrender.com

# Redeploy with new env
vercel --prod
```

---

## 📝 VERCEL CONFIGURATION FILES

### vercel.json (Already configured)
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### .env.production
```bash
VITE_API_URL=https://your-backend-url.onrender.com
```

---

## 🔧 TROUBLESHOOTING

### Issue: "Command not found: vercel"
```bash
npm install -g vercel
```

### Issue: "Build failed"
```bash
# Check Node version
node --version  # Should be 18+

# Install dependencies
cd frontend
npm install
npm run build  # Test locally
```

### Issue: "API not connecting"
- Check CORS settings on backend
- Verify VITE_API_URL is correct
- Check backend is running on Render

### Issue: "Environment variable not working"
```bash
# Redeploy after setting env vars
vercel --prod
```

---

## 📊 DEPLOYMENT CHECKLIST

### Frontend (Vercel)
- [ ] Vercel CLI installed
- [ ] Logged into Vercel
- [ ] Frontend deployed
- [ ] VITE_API_URL set
- [ ] Production build working

### Backend (Render)
- [ ] Render account created
- [ ] PostgreSQL database created
- [ ] Web service created
- [ ] Environment variables set
- [ ] CORS configured
- [ ] Backend deployed and running

### Testing
- [ ] Frontend loads on Vercel URL
- [ ] API connection working
- [ ] Dashboard shows data
- [ ] All features functional

---

## 💰 COST BREAKDOWN

### Free Tier Limits

**Vercel (Frontend)**
- ✅ Free forever
- 100 GB bandwidth/month
- Unlimited deployments
- Custom domains

**Render (Backend + Database)**
- ✅ Free tier available
- Backend: 750 hours/month
- Database: 90 days free, then $7/month
- Sleeps after 15 min inactivity

**Total Cost:**
- First 90 days: **$0**
- After 90 days: **$7/month** (database only)

---

## 🌐 ALTERNATIVE BACKENDS

### Railway (Alternative to Render)
- Free $5 credit/month
- No sleep time
- Easy PostgreSQL setup
- Deploy: https://railway.app

### Heroku (Paid)
- $7/month for backend
- $9/month for database
- No sleep time
- Deploy: https://heroku.com

### Fly.io (Alternative)
- Free tier available
- Global edge deployment
- PostgreSQL included
- Deploy: https://fly.io

---

## 📞 SUPPORT

### Vercel Issues
- Docs: https://vercel.com/docs
- Support: https://vercel.com/support

### Render Issues
- Docs: https://render.com/docs
- Support: https://render.com/support

---

## 🎉 QUICK START (5 MINUTES)

```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Go to frontend
cd frontend

# 3. Login
vercel login

# 4. Deploy
vercel --prod

# 5. Set backend URL (use localhost for now)
vercel env add VITE_API_URL production
# Enter: http://localhost:8000

# 6. Redeploy
vercel --prod
```

**Your frontend is now live on Vercel!**

For full stack, follow "Option 2" above.

---

**Note:** Backend deployment to Render takes 10-15 minutes for first deploy.
