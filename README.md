# Smart Blood Bank System

A lightweight, deployable web application for government hospital blood banks to optimize inventory management, forecast demand, and facilitate intelligent redistribution of blood products.

## Features

- **Inventory Management**: Multi-source data ingestion (CSV, manual entry, e-RaktKosh API)
- **Demand Forecasting**: ML-based predictions using Prophet/ARIMA
- **Expiry Risk Management**: Identify units at risk of expiration
- **Transfer Recommendations**: Intelligent blood redistribution between hospitals
- **Donor Management**: Search and mobilize eligible donors
- **Notification System**: SMS/Email alerts for donors
- **Role-Based Access Control**: Staff and admin user roles
- **Audit Logging**: Track sensitive actions

## Technology Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy
- **Database**: PostgreSQL 14+
- **ML**: Prophet, Pandas, NumPy
- **Testing**: pytest, Hypothesis (property-based testing)
# Smart Blood Bank System

Smart Blood Bank System is a deployable web application for hospital blood-bank teams to manage inventory, forecast demand, identify expiring units, and recommend transfers between facilities.

**Core capabilities**: inventory ingestion, ML forecasting (Prophet), expiry risk detection, transfer recommendations, donor management, and notifications.

**Stack**: Python 3.10+, FastAPI, SQLAlchemy, PostgreSQL, Vite/React frontend, Docker.

**Repository layout (high level)**

```
README.md
backend/         # FastAPI app, models, services, migrations
frontend/        # Vite + React frontend
docker/          # Dockerfiles used by compose/builds
docker-compose.yml
scripts/         # helper scripts (db init, checks, start scripts)
QUICKSTART.md
QUICK_DEPLOY.md
DEPLOYMENT_GUIDE.md
tests/
```

**Quick links**
- Backend entry: `backend/app/main.py` (FastAPI)
- Backend requirements: `backend/requirements.txt`
- Docker Compose: `docker-compose.yml`
- Quick start guide: `QUICKSTART.md`
- Quick deployment notes: `QUICK_DEPLOY.md`

**Prerequisites**
- Python 3.10+
- Docker & Docker Compose (for containerized DB / full stack)
- Git

## Quick Start (Local)

1. Clone the repo

```bash
git clone <repo-url>
cd "Smart Blood Bank System"
```

2. Copy environment template and edit values if needed

```bash
cp .env.example .env
# edit .env as required
```

3. Start PostgreSQL (Docker Compose)

```bash
docker-compose up -d db
```

4. Install Python dependencies and run migrations

```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

5. Start the backend (development)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. Open the API docs

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Quick Start (Docker Compose - Full Stack)

Start all services (db, backend, frontend):

```bash
docker-compose up -d
# tail logs
docker-compose logs -f
```

Stop services:

```bash
docker-compose down
```

Notes:
- Compose builds the backend using `docker/Dockerfile.backend` and the frontend using `frontend/Dockerfile`.
- Default DB credentials and ports are provided via `docker-compose.yml` and `.env` variables.

## Useful Scripts
- `./start_backend.sh` — wrapper to run the backend locally (see script)
- `./update_cors.sh <origin>` — update allowed CORS origins for backend (used with ngrok/Vercel)
- `scripts/check_setup.py` — verifies environment and setup

## Testing

Run tests from the `backend` directory:

```bash
cd backend
pytest -v
```

Property-based tests are marked and can be run with markers if available:

```bash
pytest -v -m property
```

## Environment Variables

Copy `.env.example` to `.env` and update as needed. Important vars:

- `DATABASE_URL` — PostgreSQL connection string
- `SECRET_KEY` — app secret/key
- `SMS_GATEWAY_API_KEY` — optional SMS provider key
- `BACKEND_PORT`, `DB_PORT`, `FRONTEND_PORT` — ports used by Docker Compose

## Deployment Notes

- For quick local exposure use `ngrok` with `./start_backend.sh` and `./update_cors.sh` (see `QUICK_DEPLOY.md`).
- Frontend can be deployed to Vercel; set `VITE_API_URL` to your backend URL.
- Docker and Render/Railway/Heroku options are documented in `DEPLOYMENT_GUIDE.md` and `RENDER_WEB_SERVICE_DEPLOYMENT.md`.

## Contributing

1. Create a feature branch
2. Add tests for new functionality
3. Open a PR and request reviews

## License & Attribution

Government of India - Public Health Initiative (see project docs)

## Support

For issues, review the repository docs or open an issue. For urgent support, contact the project maintainers listed in the repository.
