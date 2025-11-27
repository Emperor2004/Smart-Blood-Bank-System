# 🚀 Smart Blood Bank - Deployment Guide

## Quick Deployment Options

### Option 1: Local Deployment (Recommended for Demo)

#### Prerequisites
- Python 3.10+
- Docker Desktop (for PostgreSQL)

#### Steps (5 minutes)

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt

# 2. Start PostgreSQL with Docker
docker-compose up -d

# 3. Run database migrations
cd backend
alembic upgrade head

# 4. Seed demo data (3 hospitals, 6 months data, 100 donors)
python scripts/seed_data.py

# 5. Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 6. Access the application
# API Documentation: http://localhost:8000/docs
# Health Check: http://localhost:8000/health
```

#### Test Credentials
- **Admin:** username=`admin`, password=`admin123`
- **Staff:** username=`staff1`, password=`staff123`

---

### Option 2: Cloud Deployment (Render - Free Tier)

#### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Smart Blood Bank System"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** smart-blood-bank
     - **Environment:** Python 3
     - **Build Command:** `pip install -r backend/requirements.txt`
     - **Start Command:** `cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Add PostgreSQL database (free tier)
   - Set environment variables from `.env.example`
   - Click "Create Web Service"

3. **Seed Data**
```bash
# After deployment, run via Render shell
python backend/scripts/seed_data.py
```

**Your app will be live at:** `https://smart-blood-bank.onrender.com`

---

### Option 3: Heroku Deployment

```bash
# 1. Install Heroku CLI
# Download from: https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create app
heroku create smart-blood-bank

# 4. Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# 5. Set environment variables
heroku config:set SECRET_KEY=your-secret-key-here
heroku config:set JWT_SECRET_KEY=your-jwt-secret-here
heroku config:set ENCRYPTION_KEY=your-encryption-key-here

# 6. Create Procfile
echo "web: cd backend && alembic upgrade head && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:\$PORT" > Procfile

# 7. Deploy
git push heroku main

# 8. Seed data
heroku run python backend/scripts/seed_data.py

# 9. Open app
heroku open
```

---

### Option 4: Railway Deployment

1. Go to https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Add PostgreSQL database
5. Configure environment variables
6. Deploy automatically

---

### Option 5: Docker Deployment (Production)

```bash
# 1. Build and start all services
docker-compose up -d

# 2. Run migrations
docker-compose exec backend alembic upgrade head

# 3. Seed data
docker-compose exec backend python scripts/seed_data.py

# 4. Access application
# API: http://localhost:8000/docs
```

---

## Environment Variables

Create a `.env` file with these variables:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/smart_blood_bank

# Security (Generate secure keys!)
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
ENCRYPTION_KEY=your-encryption-key-change-this

# Application
ENVIRONMENT=production
DEBUG=false

# Forecasting
FORECAST_HORIZON_DAYS=7
FORECAST_HISTORY_DAYS=180

# Transfers
TRANSFER_RADIUS_KM=50
TRANSFER_WEIGHT_EXPIRY=0.6
TRANSFER_WEIGHT_DISTANCE=0.2
TRANSFER_WEIGHT_SURPLUS=0.2

# Expiry
EXPIRY_RISK_THRESHOLD_DAYS=3

# Donors
DONOR_ELIGIBILITY_DAYS=90

# Background Jobs
SCHEDULER_ENABLED=true
FORECAST_JOB_HOUR=2
FORECAST_JOB_MINUTE=0
```

---

## Generating Secure Keys

```python
# Run this in Python to generate secure keys
import secrets

print("SECRET_KEY:", secrets.token_urlsafe(32))
print("JWT_SECRET_KEY:", secrets.token_urlsafe(32))
print("ENCRYPTION_KEY:", secrets.token_urlsafe(32))
```

---

## Post-Deployment Checklist

- [ ] Database migrations applied
- [ ] Demo data seeded
- [ ] API documentation accessible at `/docs`
- [ ] Health check working at `/health`
- [ ] Test login with admin credentials
- [ ] Upload sample CSV file
- [ ] Generate a forecast
- [ ] Get transfer recommendations
- [ ] Search for donors
- [ ] Background jobs running (check logs)

---

## Monitoring & Maintenance

### Check Application Health
```bash
curl http://your-domain.com/health
```

### View Logs
```bash
# Docker
docker-compose logs -f backend

# Heroku
heroku logs --tail

# Render
# View logs in dashboard
```

### Run Migrations
```bash
# Local
cd backend && alembic upgrade head

# Heroku
heroku run alembic upgrade head

# Docker
docker-compose exec backend alembic upgrade head
```

### Backup Database
```bash
# PostgreSQL backup
pg_dump smart_blood_bank > backup.sql

# Restore
psql smart_blood_bank < backup.sql
```

---

## Troubleshooting

### Issue: Database connection failed
**Solution:** Check DATABASE_URL environment variable

### Issue: Import errors
**Solution:** Ensure all dependencies installed: `pip install -r backend/requirements.txt`

### Issue: Migration errors
**Solution:** Reset database and re-run migrations:
```bash
alembic downgrade base
alembic upgrade head
```

### Issue: Port already in use
**Solution:** Change port: `uvicorn app.main:app --port 8001`

---

## Performance Optimization

### For Production:

1. **Use Gunicorn with multiple workers**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

2. **Enable caching** (Redis)
```bash
pip install redis
# Configure in app/config.py
```

3. **Database connection pooling**
Already configured in `app/database.py`

4. **Enable HTTPS**
Use Nginx or cloud provider SSL

---

## Scaling

### Horizontal Scaling
- Deploy multiple instances behind a load balancer
- Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
- Add Redis for caching

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Optimize database queries
- Add database indexes

---

## Security Checklist

- [x] JWT authentication enabled
- [x] Passwords hashed with bcrypt
- [x] Sensitive data encrypted
- [x] SQL injection prevention
- [x] CORS configured
- [ ] HTTPS enabled (configure in production)
- [ ] Rate limiting (add if needed)
- [ ] API key rotation policy

---

## Support

For issues:
1. Check logs
2. Review documentation
3. Test with Swagger UI at `/docs`
4. Verify environment variables

---

**Deployment Status:** ✅ Ready for Production  
**Estimated Setup Time:** 5-10 minutes  
**Recommended:** Start with Render (free tier) for demos
