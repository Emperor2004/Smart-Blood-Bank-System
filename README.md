# 🩸 Smart Blood Bank System

A production-ready web application for government hospital blood banks to optimize inventory management, forecast demand, and facilitate intelligent redistribution of blood products.

[![Status](https://img.shields.io/badge/status-production--ready-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)]()
[![React](https://img.shields.io/badge/React-18.2-61dafb)]()
[![License](https://img.shields.io/badge/license-Government%20of%20India-orange)]()

---

## 🎯 Overview

Smart Blood Bank System is a **fully developed, production-ready** application for hospital blood-bank teams to manage inventory, forecast demand, identify expiring units, and recommend transfers between facilities.

**Status:** ✅ 100% Complete | All features implemented | UI/UX optimized | Deployment ready

---

## ✨ Key Features

### 📊 Core Functionality
- **Inventory Management** - Multi-source data ingestion (CSV upload, manual entry, e-RaktKosh API)
- **ML Demand Forecasting** - Prophet-based time series predictions with 95% confidence intervals
- **Expiry Risk Detection** - Automatic identification of units expiring within 3 days
- **Transfer Recommendations** - Intelligent redistribution based on urgency, distance, and surplus
- **Donor Management** - Search, filter, and mobilize eligible donors with geospatial queries
- **Real-time Dashboard** - Live statistics, blood group distribution, and risk alerts

### 🔔 Notifications
- **SMS Integration** - Twilio-powered donor notifications
- **Email Alerts** - SMTP-based email notifications
- **Simulation Mode** - Test without credentials (prints to console)

### 🔐 Security & Compliance
- **JWT Authentication** - Secure token-based auth with role-based access control
- **Data Encryption** - Encrypted storage for sensitive donor information
- **Audit Logging** - Track all sensitive operations
- **CORS Configuration** - Secure cross-origin resource sharing

### 🎨 User Experience
- **Modern UI** - React-based responsive interface with professional design
- **Complete UI/UX** - Back buttons, tooltips, loading states, error handling
- **6 Main Views** - Home, Dashboard, Upload, Forecast, Transfers, Donors
- **Mobile Responsive** - Works on all screen sizes

---

## 🏗️ Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL 14+ with SQLAlchemy ORM
- **ML/Forecasting:** Prophet, Pandas, NumPy, Statsmodels
- **Authentication:** JWT with bcrypt password hashing
- **Background Jobs:** APScheduler for automated forecasting
- **Testing:** pytest, Hypothesis (property-based testing)

### Frontend
- **Framework:** React 18.2 with TypeScript
- **Build Tool:** Vite 5.0
- **Styling:** Pure CSS (no external UI libraries)
- **State Management:** React Hooks

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Database Migrations:** Alembic
- **API Documentation:** OpenAPI/Swagger (auto-generated)

---

## 📁 Project Structure

```
Smart Blood Bank System/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # 9 API route modules
│   │   ├── models/            # 10 database models
│   │   ├── repositories/      # 7 data access layers
│   │   ├── schemas/           # 9 Pydantic schemas
│   │   ├── services/          # 8 business logic services
│   │   └── utils/             # Authentication & encryption
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Unit & integration tests
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # 6 React components
│   │   ├── services/          # API client
│   │   └── styles.css         # Application styles
│   ├── package.json
│   └── vite.config.ts
│
├── docker/                     # Docker configurations
│   ├── Dockerfile.backend
│   └── init.sql
│
├── scripts/                    # Utility scripts
│   ├── check_setup.py
│   └── init_db.py
│
├── test_samples/               # Sample CSV files
├── docker-compose.yml          # Full stack orchestration
├── .env.example                # Environment template
└── README.md                   # This file
```

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

Start all services with one command:

```bash
# Clone repository
git clone <repo-url>
cd "Smart Blood Bank System"

# Copy environment file
cp .env.example .env

# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

```bash
# 1. Start PostgreSQL
docker-compose up -d db

# 2. Setup Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head

# 3. Start Backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 4. Setup Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Option 3: Quick Start Script

```bash
./start_local.sh
```

---

## 📊 API Endpoints

### Core Services (40+ endpoints)

**Authentication**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/me` - Get current user

**Inventory**
- `POST /api/inventory/upload` - Upload CSV
- `GET /api/inventory` - List inventory
- `POST /api/inventory` - Add record
- `GET /api/inventory/{id}` - Get record

**Dashboard**
- `GET /api/dashboard/summary` - Statistics
- `GET /api/dashboard/high-risk-inventory` - Expiring units

**Forecasting**
- `GET /api/forecast` - Get predictions
- `POST /api/forecast/generate` - Generate forecast

**Transfers**
- `GET /api/transfers/recommendations` - Get recommendations
- `POST /api/transfers/approve` - Approve transfer

**Donors**
- `GET /api/donors/search` - Search donors
- `POST /api/donors` - Register donor
- `PUT /api/donors/{id}/eligibility` - Update eligibility

**Notifications**
- `POST /api/notifications/donor` - Send notification
- `GET /api/notifications` - List notifications

**e-RaktKosh**
- `POST /api/eraktkosh/sync/{hospital_id}` - Sync inventory
- `GET /api/eraktkosh/status` - Integration status

**Hospitals**
- `GET /api/hospitals` - List hospitals
- `POST /api/hospitals` - Add hospital

**Full API Documentation:** http://localhost:8000/docs

---

## ⚙️ Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://bloodbank:bloodbank123@localhost:5432/smart_blood_bank

# Security
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key-32-bytes

# SMS Notifications (Optional - Twilio)
SMS_GATEWAY_ENABLED=False
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Email Notifications (Optional - SMTP)
EMAIL_ENABLED=False
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# e-RaktKosh Integration (Optional)
ERAKTKOSH_API_ENABLED=False
ERAKTKOSH_API_KEY=your_api_key

# CORS
CORS_ORIGINS=http://localhost:3000,https://your-app.vercel.app
```

**Generate Secure Keys:**
```bash
openssl rand -hex 32
```

**See:** `CONFIGURATION_GUIDE.md` for detailed setup instructions.

---

## 🧪 Testing

```bash
cd backend
pytest -v                    # Run all tests
pytest -v -m property        # Run property-based tests
pytest --cov=app             # Run with coverage
```

**Test Coverage:**
- CSV ingestion and validation
- Blood group normalization (40+ variants)
- Duplicate detection
- API endpoint testing
- Database operations

---

## 📦 Deployment

### Frontend → Vercel (Free)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

### Backend → Render (Free tier available)

```bash
# See detailed guide
cat RENDER_WEB_SERVICE_DEPLOYMENT.md
```

### Full Stack Deployment

See comprehensive guides:
- `VERCEL_DEPLOYMENT_GUIDE.md` - Frontend deployment
- `RENDER_WEB_SERVICE_DEPLOYMENT.md` - Backend deployment
- `DEPLOYMENT_GUIDE.md` - General deployment options

**Quick Deploy:**
```bash
./deploy_vercel.sh  # Deploy frontend to Vercel
```

---

## 📚 Documentation

### Getting Started
- **QUICKSTART.md** - Quick start guide
- **CONFIGURATION_GUIDE.md** - Configuration details
- **FULLY_DEVELOPED.md** - Feature completion status

### Deployment
- **VERCEL_DEPLOYMENT_GUIDE.md** - Vercel deployment (frontend)
- **RENDER_WEB_SERVICE_DEPLOYMENT.md** - Render deployment (backend)
- **DEPLOYMENT_GUIDE.md** - General deployment guide

### System Information
- **SYSTEM_STATUS_REPORT.md** - Live system status
- **UI_UX_IMPROVEMENTS_COMPLETE.md** - UI/UX documentation
- **CLEANUP_SUMMARY.md** - Project cleanup details

---

## 🎨 Features Highlights

### Dashboard
- Real-time blood unit statistics
- High-risk inventory alerts (expiring ≤3 days)
- Blood group distribution
- Hospital count and metrics

### Inventory Upload
- Drag & drop CSV upload
- Real-time validation
- Blood group normalization (handles 40+ variants)
- Duplicate detection
- Error reporting with line numbers

### Demand Forecasting
- Prophet ML model with 180-day training
- 7-30 day predictions
- 95% confidence intervals
- MAE/MAPE evaluation metrics
- Visual forecast charts

### Transfer Recommendations
- Geospatial matching (Haversine distance)
- 50km radius search
- Urgency scoring (expiry 60%, distance 20%, surplus 20%)
- ETA calculation
- Color-coded urgency levels

### Donor Management
- Encrypted contact information
- 90-day eligibility tracking
- Geospatial radius search
- Blood group filtering
- SMS/Email notifications

---

## 🔧 Utility Scripts

```bash
./start_local.sh          # Start all services locally
./stop_local.sh           # Stop all services
./run_tests.sh            # Run test suite
./verify_complete.sh      # Verify installation
./cleanup_project.sh      # Clean unnecessary files
./deploy_vercel.sh        # Deploy to Vercel
```

---

## 💡 Usage Examples

### Upload Inventory CSV

```bash
curl -X POST http://localhost:8000/api/inventory/upload \
  -F "file=@test_samples/valid_inventory.csv"
```

### Get Dashboard Summary

```bash
curl http://localhost:8000/api/dashboard/summary
```

### Generate Forecast

```bash
curl "http://localhost:8000/api/forecast?hospital_id=H001&blood_group=A%2B&component=RBC&days=7"
```

### Search Donors

```bash
curl "http://localhost:8000/api/donors/search?blood_group=O%2B&eligible_only=true"
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check database connection
docker-compose up -d db
docker exec blood_bank_db pg_isready -U bloodbank

# Check logs
tail -f backend_run.log
```

### Frontend build fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Database migration issues
```bash
cd backend
alembic downgrade -1
alembic upgrade head
```

---

## 📊 System Requirements

### Minimum
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Storage:** 10 GB
- **OS:** Linux, macOS, Windows (with WSL2)

### Recommended
- **CPU:** 4 cores
- **RAM:** 8 GB
- **Storage:** 20 GB
- **OS:** Linux (Ubuntu 20.04+)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Guidelines:**
- Add tests for new features
- Update documentation
- Follow existing code style
- Ensure all tests pass

---

## 📄 License

Government of India - Public Health Initiative

This project is developed for government hospitals to improve blood bank management and save lives.

---

## 🙏 Acknowledgments

- **Prophet** - Facebook's time series forecasting library
- **FastAPI** - Modern Python web framework
- **React** - UI library
- **PostgreSQL** - Reliable database system

---

## 📞 Support

### Documentation
- Check `QUICKSTART.md` for quick start
- See `CONFIGURATION_GUIDE.md` for setup
- Read `DEPLOYMENT_GUIDE.md` for deployment

### Issues
- Open an issue on GitHub
- Check existing documentation first
- Provide error logs and system info

### Contact
For urgent support, contact project maintainers listed in the repository.

---

## 🎯 Project Status

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** December 1, 2025

### Completion Checklist
- [x] Backend API (9 modules, 40+ endpoints)
- [x] Frontend UI (6 views, complete UI/UX)
- [x] Database schema (10 tables)
- [x] ML forecasting (Prophet integration)
- [x] SMS/Email notifications (Twilio/SMTP)
- [x] e-RaktKosh integration
- [x] Docker deployment
- [x] Vercel deployment support
- [x] Render deployment support
- [x] Complete documentation
- [x] Test suite
- [x] Security features (JWT, encryption)
- [x] Audit logging
- [x] Project cleanup

**All features implemented. System is production-ready.**

---

## 🚀 Quick Links

- **Live Demo:** Deploy to see it in action
- **API Docs:** http://localhost:8000/docs (when running)
- **Frontend:** http://localhost:3000 (when running)
- **GitHub:** [Repository URL]

---

**Built with ❤️ for saving lives through technology**
