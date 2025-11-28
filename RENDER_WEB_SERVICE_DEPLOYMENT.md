# Render Web Service Deployment Guide (Hobby Tier)

This guide walks you through deploying Smart Blood Bank to Render using the Web Service UI (manual approach). This is the most reliable method for the Hobby (free) tier.

---

## Prerequisites

- GitHub account with your Smart Blood Bank repo pushed
- Render account (free tier) — [render.com](https://render.com)
- GitHub connected to Render (authorize Render to access your repos)

---

## Deployment Architecture

You will create **3 services** in Render:

1. **PostgreSQL Database** (managed, Render-hosted)
2. **Backend API** (Web Service running `docker/Dockerfile.backend.render`)
3. **Frontend** (Web Service running `frontend/Dockerfile`)

All services will be in the same region (e.g., `oregon`) for lower latency.

---

## Step 1: Create PostgreSQL Database

### In Render Dashboard:

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **+ New** → **PostgreSQL**
3. Fill in:
   - **Name**: `smart-blood-bank-db` (or any name you prefer)
   - **Database**: `smart_blood_bank`
   - **User**: `bloodbank`
   - **Region**: Choose closest to you (e.g., `Oregon`)
   - **Version**: Latest available (e.g., 14 or 15)
   - **Plan**: **Free** (for Hobby tier)
4. Click **Create Database**

### After creation:

- Render will display the **Internal Database URL** (used by backend from within Render network)
- Example: `postgresql://bloodbank:password@dpg-xxx.render.internal:5432/smart_blood_bank`
- **Copy this URL** — you'll paste it into the backend service in Step 3.

---

## Step 2: Deploy Backend API

### In Render Dashboard:

1. Click **+ New** → **Web Service**
2. **Connect your GitHub repo**:
   - Search for `Smart-Blood-Bank-System` (or your repo name)
   - Click **Connect**
3. Fill in service settings:
   - **Name**: `smart-blood-bank-backend`
   - **Environment**: **Docker**
   - **Region**: Same as database (e.g., `Oregon`)
   - **Branch**: `main`
   - **Dockerfile path**: `docker/Dockerfile.backend.render`
   - **Dockerfile context**: `backend`
   - **Plan**: **Free** (Hobby tier)

4. Click **Advanced** (optional but recommended to see all options)

5. **Environment Variables** — Click **Add Environment Variable** for each:

   | Key | Value |
   |-----|-------|
   | `ENVIRONMENT` | `production` |
   | `DEBUG` | `False` |
   | `DATABASE_URL` | Paste the PostgreSQL URL from Step 1 |
   | `SECRET_KEY` | Generate a strong random string (32+ chars) or use `openssl rand -hex 16` |
   | `JWT_SECRET_KEY` | Generate another strong random string (32+ chars) |
   | `LOG_LEVEL` | `INFO` |
   | `SCHEDULER_ENABLED` | `True` |
   | `CORS_ORIGINS` | Will set after frontend URL is known; for now use `http://localhost:3000` |

   **Optional** (only if you'll use SMS/Email later):
   - `SMS_GATEWAY_API_KEY`
   - `TWILIO_ACCOUNT_SID`
   - `TWILIO_AUTH_TOKEN`
   - `TWILIO_PHONE_NUMBER`
   - `SMTP_USER`
   - `SMTP_PASSWORD`

6. Click **Deploy Web Service**

Render will now:
- Clone your repo
- Build the Docker image (takes ~5-10 min for first build due to Prophet dependencies)
- Start the backend service
- Assign a public URL like `https://smart-blood-bank-backend.onrender.com`

### After backend deploys (may take 10-15 min):

**Migrations run automatically!**

- The Docker image now runs `alembic upgrade head` before starting the server
- This happens on every deployment, so the database schema will be created automatically
- Check the **Logs** tab to confirm migrations ran:
  ```
  INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
  INFO  [alembic.runtime.migration] Running upgrade  -> 001_create_initial_schema, done
  ```

If you see these messages, the backend is ready!

---

## Step 3: Deploy Frontend

### In Render Dashboard:

1. Click **+ New** → **Web Service**
2. **Connect your GitHub repo** (same as backend):
   - Search for `Smart-Blood-Bank-System`
   - Click **Connect**
3. Fill in service settings:
   - **Name**: `smart-blood-bank-frontend`
   - **Environment**: **Docker**
   - **Region**: Same as backend/database (e.g., `Oregon`)
   - **Branch**: `main`
   - **Dockerfile path**: `frontend/Dockerfile`
   - **Dockerfile context**: `frontend`
   - **Plan**: **Free** (Hobby tier)

4. **Environment Variables**:
   - Click **Add Environment Variable**
   - **Key**: `VITE_BACKEND_URL`
   - **Value**: The backend URL from Step 2 (e.g., `https://smart-blood-bank-backend.onrender.com`)

5. Click **Deploy Web Service**

Render will build the frontend (takes ~3-5 min) and assign a public URL like:
- `https://smart-blood-bank-frontend.onrender.com`

---

## Step 4: Test the Deployment

### Access the frontend:

1. Open `https://smart-blood-bank-frontend.onrender.com` in your browser
2. You should see the Smart Blood Bank homepage with tabs: **Home**, **Upload Inventory**, **Forecast**

### Test the connection:

1. Go to **Upload Inventory** tab
2. Click the file input and select a test CSV (or use the sample below)
3. Click **Upload**
4. Should see success/error response from backend

### Sample CSV to test:

Create a file `sample.csv`:
```csv
record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,2026-01-01,2025-11-28
R002,H001,B-,Platelets,3,2026-01-15,2025-11-28
R003,H002,O+,Plasma,2,2025-12-15,2025-11-28
```

Upload it via the frontend.

### Test the API directly:

```bash
# Backend health
curl https://smart-blood-bank-backend.onrender.com/health

# Forecast endpoint (should return data or error, not 404)
curl "https://smart-blood-bank-backend.onrender.com/api/forecast?hospital_id=H001&blood_group=A%2B&component=RBC&days=7"
```

---

## Step 5: Update CORS for Production

Now that both services are live, update the backend CORS setting:

1. Go to the **backend** service in Render
2. Click **Environment**
3. Find the `CORS_ORIGINS` variable
4. Update the value to:
   ```
   https://smart-blood-bank-frontend.onrender.com,https://smart-blood-bank-backend.onrender.com
   ```
5. Click **Save**
6. The service will redeploy automatically (takes ~1 min)

After redeploy, the frontend should fully connect to the backend without CORS errors.

---

## Important Notes for Hobby Tier

### No Render Shell Access
- **Free tier does NOT support Render Shell** (SSH/interactive commands)
- Use the **Logs** tab to view container output
- Migrations now run automatically on every service restart
- Use the **Restart** button to trigger migrations again

### Service Spinning Down
- **Free tier services automatically spin down after 15 minutes of inactivity**
- When you access the service again, it takes ~30 seconds to wake up
- This is expected behavior and NOT a failure

### Database Persistence
- Free PostgreSQL instances are reset every 90 days
- Don't rely on persistent data for long-term storage
- For production, upgrade to a paid plan

### Limited Resources
- **Prophet forecasting** (ML training) may be slow on free tier
- If forecasting times out, consider upgrading the plan or reducing the forecast history

### Background Jobs
- **APScheduler runs but is unreliable** on free tier due to service spin-down
- Scheduled forecasting may not run consistently
- For production, enable background jobs with a paid plan

---

## Troubleshooting

### Backend won't start: "prophet" build error

**Issue**: Build fails during Docker image build with Prophet errors

**Solution**:
- Ensure you're using `docker/Dockerfile.backend.render` (not the old `.backend`)
- Check that `docker/Dockerfile.backend.render` has `build-essential`, `g++`, `make`
- If still failing, check Render build logs (click **Logs** tab on service page)

### Frontend shows "Cannot reach backend"

**Issue**: Frontend loads but API calls fail with connection error

**Solution**:
1. Verify `VITE_BACKEND_URL` env var is set correctly on frontend service
2. Check that backend is running and healthy:
   ```bash
   curl https://smart-blood-bank-backend.onrender.com/health
   ```
3. Verify CORS_ORIGINS on backend includes the frontend URL
4. Wait a few seconds — backend may be waking up from spin-down

### Database connection fails

**Issue**: Backend logs show "database does not exist" or connection timeout

**Solution**:
1. Verify `DATABASE_URL` env var is set on backend service (use the **Internal Database URL**)
2. Check Render Logs tab for the exact error
3. Verify PostgreSQL instance is running (check database service page)
4. Restart the backend service — migrations will re-run on startup

### Migrations fail or hang

**Issue**: Logs show alembic errors or service keeps restarting

**Solution**:
1. Check Logs tab for the specific alembic error
2. Common issues: missing `DATABASE_URL`, wrong credentials, PostgreSQL not ready
3. Fix the env var and restart the service

---

## Viewing Logs and Debugging

Since Render Shell is not available on free tier, use the **Logs** tab:

1. Go to the backend service page in Render
2. Click **Logs** tab
3. Scroll to see real-time output from the Docker container

**Look for:**
- Alembic migration messages (database schema creation)
- Gunicorn startup message: `Listening at: http://0.0.0.0:PORT`
- Any error messages

**To restart the service:**
- Click the backend service name → **Restart** button (top right)
- This will re-run the Docker container, including migrations

---

## Next Steps (Optional Enhancements)

### Enable Custom Domain
1. Render → Backend service → **Settings** → **Custom Domain**
2. Point your domain to Render

### Set Up Monitoring
1. Render → Service → **Logs** tab (view real-time logs)
2. Set up email alerts (Render dashboard → Settings → Notifications)

### Upgrade to Paid Plan
For production:
- Use a **paid PostgreSQL instance** (persistent data, no 90-day resets)
- Use a **Standard/Pro plan** for backend/frontend (no spin-down, better performance)

---

## Quick Reference: Service URLs After Deployment

| Service | URL |
|---------|-----|
| Frontend | `https://smart-blood-bank-frontend.onrender.com` |
| Backend API | `https://smart-blood-bank-backend.onrender.com` |
| Backend Health | `https://smart-blood-bank-backend.onrender.com/health` |
| API Docs (Swagger) | `https://smart-blood-bank-backend.onrender.com/docs` |

---

## Summary

You now have a fully deployed Smart Blood Bank system on Render:

1. ✅ PostgreSQL database running on Render
2. ✅ Backend API serving on Hobby tier with migrations applied
3. ✅ Frontend React app deployed and connected to backend
4. ✅ All services accessible from public URLs
5. ✅ CORS properly configured for production

The app is ready to test! Start with the frontend and try uploading an inventory CSV or viewing the forecast. 🚀
