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
- **Deployment**: Docker, Docker Compose

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── repositories/ # Data access layer
│   │   ├── services/     # Business logic
│   │   ├── config.py     # Configuration
│   │   └── main.py       # FastAPI app
│   ├── alembic/          # Database migrations
│   ├── requirements.txt  # Python dependencies
│   └── alembic.ini       # Alembic configuration
├── frontend/             # Frontend application (TBD)
├── tests/                # Test files
├── scripts/              # Utility scripts
├── docker/               # Docker configurations
├── docker-compose.yml    # Docker Compose setup
└── .env.example          # Environment variables template
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- PostgreSQL 14+ (if not using Docker)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd smart-blood-bank
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start PostgreSQL with Docker Compose**
   ```bash
   docker-compose up -d db
   ```

4. **Install Python dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

7. **Access the API**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

### Using Docker Compose (Full Stack)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Running Tests

```bash
cd backend
pytest tests/ -v
```

### Running Property-Based Tests

```bash
cd backend
pytest tests/ -v -m property
```

## Environment Variables

See `.env.example` for all available configuration options. Key variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Application secret key
- `SMS_GATEWAY_API_KEY`: Twilio/AWS SNS API key (optional)
- `FORECAST_HORIZON_DAYS`: Default forecast period (default: 7)
- `TRANSFER_RADIUS_KM`: Search radius for transfers (default: 50)

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Deployment

### Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create smart-blood-bank

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

### Render / Railway

1. Connect your Git repository
2. Set environment variables from `.env.example`
3. Deploy with one click

## Development Workflow

1. Create a new branch for your feature
2. Implement changes following the task list in `.kiro/specs/smart-blood-bank/tasks.md`
3. Write tests (unit tests and property-based tests)
4. Run tests and ensure they pass
5. Submit pull request

## License

Government of India - Public Health Initiative

## Support

For issues and questions, please contact the development team.
