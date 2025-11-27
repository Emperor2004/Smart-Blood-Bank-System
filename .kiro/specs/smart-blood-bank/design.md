# Design Document

## Overview

The Smart Blood Bank system is a full-stack web application built with a Python backend (Flask/FastAPI), PostgreSQL database, and a lightweight frontend (React or Streamlit for MVP). The system consists of five major subsystems:

1. **Data Ingestion Layer**: Handles CSV uploads, manual entry, and e-RaktKosh API integration
2. **Inventory Management**: Stores and queries blood inventory with filtering capabilities
3. **Forecasting Engine**: ML-based demand prediction using Prophet/ARIMA
4. **Transfer Recommendation Engine**: Optimization algorithm for blood redistribution
5. **Donor Management & Notification**: Donor registry and mobilization system

The architecture follows a layered approach with clear separation between data access, business logic, and presentation layers. The system is designed for deployment on cloud platforms (Heroku/Render) with Docker containerization.

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
│  (React/Streamlit - Low bandwidth optimized)                │
│  - Dashboard  - Inventory  - Forecasts  - Transfers         │
│  - Donors     - Settings   - Logs                           │
└─────────────────┬───────────────────────────────────────────┘
                  │ REST API
┌─────────────────▼───────────────────────────────────────────┐
│                      API Gateway Layer                       │
│  (Flask/FastAPI with authentication middleware)             │
│  - Route handlers  - Request validation  - RBAC             │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    Business Logic Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Inventory   │  │  Forecast    │  │  Transfer    │     │
│  │  Service     │  │  Service     │  │  Service     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Donor       │  │  Notification│  │  Expiry      │     │
│  │  Service     │  │  Service     │  │  Service     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    Data Access Layer                         │
│  (Repository pattern with SQLAlchemy ORM)                   │
│  - Hospital Repo  - Inventory Repo  - Usage Repo            │
│  - Donor Repo     - Forecast Repo   - Transfer Repo         │
└─────────────────┬───────────────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    PostgreSQL Database                       │
│  Tables: hospitals, inventory, usage, donors, forecasts,    │
│          transfers, audit_logs, users                        │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    Background Jobs Layer                      │
│  - Daily forecast generation (scheduled via APScheduler)     │
│  - Expiry risk calculation                                   │
│  - Transfer recommendation generation                        │
│  - Model drift monitoring                                    │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    External Integrations                      │
│  - e-RaktKosh API (read-only)                               │
│  - SMS Gateway (Twilio/AWS SNS)                             │
│  - Email Service (SendGrid/SMTP)                            │
└──────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.10+
- FastAPI (REST API framework)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- Prophet or statsmodels (time-series forecasting)
- Pandas & NumPy (data processing)
- APScheduler (background jobs)
- Pydantic (data validation)

**Database:**
- PostgreSQL 14+
- PostGIS extension (for geospatial queries)

**Frontend:**
- React 18+ with TypeScript (production) OR Streamlit (MVP prototype)
- Chart.js or Recharts (visualization)
- Leaflet (map view)
- Tailwind CSS (styling)

**Deployment:**
- Docker & Docker Compose
- Gunicorn (WSGI server)
- Nginx (reverse proxy, optional)
- Heroku/Render/Railway (cloud hosting)

## Components and Interfaces

### 1. Data Ingestion Component

**Responsibilities:**
- Parse and validate CSV files
- Normalize blood group values
- Detect and reject duplicates
- Interface with e-RaktKosh API

**Interfaces:**

```python
class IngestionService:
    def upload_inventory_csv(self, file: UploadFile) -> IngestionResult
    def validate_csv_format(self, df: DataFrame) -> ValidationResult
    def normalize_blood_group(self, blood_group: str) -> str
    def check_duplicates(self, records: List[InventoryRecord]) -> List[str]
    def ingest_from_eraktkosh(self, hospital_id: str) -> IngestionResult
```

**CSV Format Validation:**
- Required columns: record_id, hospital_id, blood_group, component, units, unit_expiry_date, collection_date
- Blood group normalization: A+/A Positive → A+, O-/O Negative → O-
- Date format: YYYY-MM-DD
- Duplicate detection: Check record_id uniqueness

### 2. Inventory Management Component

**Responsibilities:**
- CRUD operations for inventory
- Multi-criteria filtering
- Stock level queries

**Interfaces:**

```python
class InventoryService:
    def get_inventory(self, filters: InventoryFilters) -> List[InventoryRecord]
    def add_inventory_record(self, record: InventoryRecord) -> str
    def update_inventory(self, record_id: str, updates: dict) -> bool
    def get_stock_summary(self, hospital_id: str) -> StockSummary
    def get_units_by_expiry_range(self, days: int) -> List[InventoryRecord]
```

### 3. Forecasting Engine Component

**Responsibilities:**
- Train time-series models on historical usage
- Generate 7-day and 30-day forecasts
- Calculate confidence intervals
- Store and retrieve forecasts

**Interfaces:**

```python
class ForecastService:
    def train_model(self, hospital_id: str, blood_group: str, component: str) -> Model
    def generate_forecast(self, hospital_id: str, blood_group: str, 
                         component: str, days: int) -> ForecastResult
    def get_forecast(self, hospital_id: str, blood_group: str, 
                    days: int) -> ForecastResult
    def evaluate_model(self, model: Model, test_data: DataFrame) -> ModelMetrics
```

**ML Pipeline:**

```
Historical Usage Data (180 days)
    ↓
Preprocessing (fill missing dates, aggregate by day)
    ↓
Train/Test Split (last 30 days = test)
    ↓
Model Training (Prophet/ARIMA)
    ↓
Evaluation (MAE, MAPE)
    ↓
Forecast Generation (7d/30d with confidence intervals)
    ↓
Store in Database
```

**Prophet Model Configuration:**
```python
model = Prophet(
    yearly_seasonality=False,
    weekly_seasonality=True,
    daily_seasonality=False,
    interval_width=0.95  # 95% confidence intervals
)
```

### 4. Expiry Risk Component

**Responsibilities:**
- Calculate days to expiry
- Compute expiry risk scores
- Flag high-risk units

**Interfaces:**

```python
class ExpiryService:
    def calculate_expiry_risk(self, inventory_record: InventoryRecord) -> float
    def get_high_risk_units(self, threshold_days: int = 3) -> List[InventoryRecord]
    def get_expiry_summary(self) -> ExpirySummary
```

**Risk Calculation Formula:**
```
days_to_expiry = unit_expiry_date - current_date
expiry_risk_score = (1 / (days_to_expiry + 1)) * units
high_risk = days_to_expiry <= threshold (default: 3 days)
```

### 5. Transfer Recommendation Engine Component

**Responsibilities:**
- Identify deficit and surplus hospitals
- Calculate transfer urgency scores
- Rank transfer recommendations
- Estimate transfer logistics

**Interfaces:**

```python
class TransferService:
    def generate_recommendations(self, hospital_id: str = None) -> List[TransferRecommendation]
    def calculate_urgency_score(self, transfer: TransferCandidate) -> float
    def find_nearby_hospitals(self, hospital_id: str, radius_km: float) -> List[Hospital]
    def approve_transfer(self, transfer_id: str, admin_id: str) -> bool
    def estimate_eta(self, distance_km: float) -> timedelta
```

**Transfer Recommendation Algorithm:**

```
For each hospital H:
  1. Get forecast for next D days (configurable, default 7)
  2. Get current inventory
  3. Calculate deficit: deficit = forecast - inventory (where < 0)
  
  For each deficit blood group G:
    4. Query nearby hospitals within radius R (default 50km)
    5. Filter hospitals with surplus: surplus = inventory - forecast (where > threshold)
    6. For each candidate transfer:
       - Normalize days_to_expiry: norm_expiry = days_to_expiry / max_days
       - Normalize distance: norm_distance = distance / max_distance
       - Normalize surplus: norm_surplus = surplus / max_surplus
       - Calculate score: urgency = w1*(1-norm_expiry) + w2*(1-norm_distance) + w3*norm_surplus
         (default weights: w1=0.6, w2=0.2, w3=0.2)
    7. Rank by urgency score (descending)
    8. Calculate ETA: eta = distance / 40 km/h
    9. Return top N recommendations
```

### 6. Donor Management Component

**Responsibilities:**
- Register and manage donors
- Search eligible donors
- Calculate eligibility based on last donation

**Interfaces:**

```python
class DonorService:
    def register_donor(self, donor: DonorRegistration) -> str
    def search_donors(self, blood_group: str, radius_km: float, 
                     eligible_only: bool, hospital_location: Location) -> List[Donor]
    def update_eligibility(self, donor_id: str) -> bool
    def calculate_eligibility(self, last_donation_date: date) -> bool
```

**Eligibility Calculation:**
```
eligible = (current_date - last_donation_date) > 90 days
```

### 7. Notification Component

**Responsibilities:**
- Generate notification messages from templates
- Send SMS/Email via external gateways
- Log notification events
- Simulate notifications when gateway unavailable

**Interfaces:**

```python
class NotificationService:
    def send_donor_notification(self, donor_id: str, template_id: str, 
                                context: dict) -> NotificationResult
    def generate_message(self, template_id: str, context: dict) -> str
    def log_notification(self, notification: NotificationLog) -> None
    def simulate_send(self, message: str, recipient: str) -> None
```

**SMS Template:**
```
"Urgent! {hospital_name} needs {blood_group} donors. If eligible, please contact {phone} or click {link}."
```

### 8. Authentication & Authorization Component

**Responsibilities:**
- User authentication
- Role-based access control
- Audit logging

**Interfaces:**

```python
class AuthService:
    def authenticate(self, username: str, password: str) -> User
    def authorize(self, user: User, resource: str, action: str) -> bool
    def log_action(self, user_id: str, action: str, details: dict) -> None
```

**Roles:**
- **Staff**: Can view inventory, manage donors, view forecasts (read-only)
- **Admin**: All staff permissions + approve transfers, modify settings, view audit logs

## Data Models

### Database Schema

```sql
-- Hospitals Table
CREATE TABLE hospitals (
    hospital_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    contact_name VARCHAR(255),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inventory Table
CREATE TABLE inventory (
    record_id VARCHAR(50) PRIMARY KEY,
    hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    blood_group VARCHAR(5) NOT NULL,
    component VARCHAR(20) NOT NULL,
    units INTEGER NOT NULL,
    unit_expiry_date DATE NOT NULL,
    collection_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_blood_group CHECK (blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')),
    CONSTRAINT chk_component CHECK (component IN ('RBC', 'Platelets', 'Plasma')),
    CONSTRAINT chk_units CHECK (units > 0)
);

-- Usage Table
CREATE TABLE usage (
    usage_id SERIAL PRIMARY KEY,
    hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    blood_group VARCHAR(5) NOT NULL,
    component VARCHAR(20) NOT NULL,
    units_used INTEGER NOT NULL,
    usage_date DATE NOT NULL,
    purpose VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_purpose CHECK (purpose IN ('surgery', 'emergency', 'other'))
);

-- Donors Table
CREATE TABLE donors (
    donor_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    blood_group VARCHAR(5) NOT NULL,
    last_donation_date DATE,
    eligible BOOLEAN DEFAULT TRUE,
    location_lat DECIMAL(10, 8),
    location_lon DECIMAL(11, 8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Forecasts Table
CREATE TABLE forecasts (
    forecast_id SERIAL PRIMARY KEY,
    hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    blood_group VARCHAR(5) NOT NULL,
    component VARCHAR(20) NOT NULL,
    forecast_date DATE NOT NULL,
    predicted_units DECIMAL(10, 2) NOT NULL,
    lower_bound DECIMAL(10, 2),
    upper_bound DECIMAL(10, 2),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(hospital_id, blood_group, component, forecast_date, generated_at)
);

-- Transfers Table
CREATE TABLE transfers (
    transfer_id SERIAL PRIMARY KEY,
    source_hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    destination_hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    blood_group VARCHAR(5) NOT NULL,
    component VARCHAR(20) NOT NULL,
    units INTEGER NOT NULL,
    urgency_score DECIMAL(5, 3),
    distance_km DECIMAL(6, 2),
    eta_minutes INTEGER,
    status VARCHAR(20) DEFAULT 'pending',
    approved_by VARCHAR(50),
    approved_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_status CHECK (status IN ('pending', 'approved', 'completed', 'cancelled'))
);

-- Audit Logs Table
CREATE TABLE audit_logs (
    log_id SERIAL PRIMARY KEY,
    user_id VARCHAR(50),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(50),
    details JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL,
    hospital_id VARCHAR(50) REFERENCES hospitals(hospital_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_role CHECK (role IN ('staff', 'admin'))
);

-- Notifications Table
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    donor_id INTEGER REFERENCES donors(donor_id),
    template_id VARCHAR(50),
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_notification_status CHECK (status IN ('pending', 'sent', 'failed', 'simulated'))
);

-- Create indexes for common queries
CREATE INDEX idx_inventory_hospital ON inventory(hospital_id);
CREATE INDEX idx_inventory_blood_group ON inventory(blood_group);
CREATE INDEX idx_inventory_expiry ON inventory(unit_expiry_date);
CREATE INDEX idx_usage_hospital_date ON usage(hospital_id, usage_date);
CREATE INDEX idx_donors_blood_group ON donors(blood_group);
CREATE INDEX idx_donors_eligible ON donors(eligible);
CREATE INDEX idx_forecasts_hospital_date ON forecasts(hospital_id, forecast_date);
CREATE INDEX idx_transfers_status ON transfers(status);
```

### Python Data Models (Pydantic)

```python
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List
from enum import Enum

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class Component(str, Enum):
    RBC = "RBC"
    PLATELETS = "Platelets"
    PLASMA = "Plasma"

class Purpose(str, Enum):
    SURGERY = "surgery"
    EMERGENCY = "emergency"
    OTHER = "other"

class Hospital(BaseModel):
    hospital_id: str
    name: str
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]

class InventoryRecord(BaseModel):
    record_id: str
    hospital_id: str
    blood_group: BloodGroup
    component: Component
    units: int = Field(gt=0)
    unit_expiry_date: date
    collection_date: date

class UsageRecord(BaseModel):
    hospital_id: str
    blood_group: BloodGroup
    component: Component
    units_used: int = Field(gt=0)
    usage_date: date
    purpose: Purpose

class Donor(BaseModel):
    donor_id: Optional[int]
    name: str
    phone: str
    email: Optional[str]
    blood_group: BloodGroup
    last_donation_date: Optional[date]
    eligible: bool = True
    location_lat: Optional[float]
    location_lon: Optional[float]

class ForecastPoint(BaseModel):
    date: date
    predicted: float
    lower: float
    upper: float

class ForecastResult(BaseModel):
    hospital_id: str
    blood_group: BloodGroup
    component: Component
    forecast: List[ForecastPoint]
    generated_at: datetime

class TransferRecommendation(BaseModel):
    transfer_id: Optional[int]
    source_hospital_id: str
    source_hospital_name: str
    destination_hospital_id: str
    destination_hospital_name: str
    blood_group: BloodGroup
    component: Component
    units: int
    urgency_score: float
    distance_km: float
    eta_minutes: int
    status: str = "pending"

class InventoryFilters(BaseModel):
    hospital_id: Optional[str]
    blood_group: Optional[BloodGroup]
    component: Optional[Component]
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*


### Property Reflection

After analyzing all acceptance criteria, I've identified several areas where properties can be consolidated:

**Consolidation opportunities:**
- Properties 2.2, 2.3, 2.4 (individual filters) are subsumed by Property 2.5 (combined filters)
- Properties 3.1 and 3.2 (7-day and 30-day forecasts) can be combined into a single parameterized property
- Properties 5.4 (default weights) is validated by Property 5.3 (scoring formula)
- Properties 9.1 and 9.2 (role permissions) can be combined into a single RBAC property

**Properties to keep as separate:**
- CSV validation, normalization, and duplicate detection are distinct concerns
- Expiry risk calculation steps are sequential and should be tested separately
- Transfer recommendation steps build on each other and warrant individual properties
- Donor search filters test different algorithms (string match vs geospatial)

### Correctness Properties

**Property 1: CSV validation and import**
*For any* CSV file uploaded to the system, all records with valid format (correct columns, valid blood groups, valid dates, positive units) should be imported into the database, and all records with invalid format should be rejected with logged reasons.
**Validates: Requirements 1.1, 1.2, 1.3**

**Property 2: Blood group normalization**
*For any* blood group string that is a standard variation (e.g., "A Positive", "A+", "a+"), the normalization function should return the canonical form (e.g., "A+"), and for any unrecognizable string, it should return an error.
**Validates: Requirements 1.2**

**Property 3: Inventory filtering composition**
*For any* combination of filters (hospital_id, blood_group, component), the returned inventory records should match all specified criteria, and the result should be equivalent to applying filters sequentially in any order.
**Validates: Requirements 2.2, 2.3, 2.4, 2.5**

**Property 4: Forecast generation structure**
*For any* hospital, blood group, component, and forecast horizon (7 or 30 days), the forecast result should contain exactly that many daily predictions, each with a date, predicted value, lower bound, and upper bound where lower ≤ predicted ≤ upper.
**Validates: Requirements 3.1, 3.2, 3.3, 3.4**

**Property 5: Historical data aggregation**
*For any* set of usage records, aggregating by hospital, blood group, component, and date should produce daily totals where the sum of aggregated units equals the sum of original units_used.
**Validates: Requirements 3.5**

**Property 6: Expiry risk calculation**
*For any* inventory record, the expiry risk score should equal (1 / (days_to_expiry + 1)) * units, where days_to_expiry = unit_expiry_date - current_date, and the record should be flagged as high-risk if and only if days_to_expiry ≤ configured threshold.
**Validates: Requirements 4.1, 4.2, 4.3**

**Property 7: Deficit and surplus calculation**
*For any* hospital with inventory and forecast data, deficit blood groups should have (forecast - inventory) > 0, and surplus blood groups should have (inventory - forecast) ≥ configured threshold.
**Validates: Requirements 5.1, 5.2**

**Property 8: Transfer urgency scoring**
*For any* transfer candidate with expiry days, distance, and surplus values, the urgency score should equal w1*(1 - norm_expiry) + w2*(1 - norm_distance) + w3*norm_surplus, where normalization divides by the maximum value in the candidate set and weights sum to 1.0.
**Validates: Requirements 5.3, 5.4**

**Property 9: Transfer ETA calculation**
*For any* distance in kilometers, the estimated time of arrival in minutes should equal (distance / 40) * 60, rounded to the nearest integer.
**Validates: Requirements 5.5**

**Property 10: Transfer approval inventory update**
*For any* approved transfer of N units from hospital A to hospital B, the source hospital's inventory should decrease by N units and the destination hospital's inventory should increase by N units for the specified blood group and component.
**Validates: Requirements 5.7**

**Property 11: Donor search filtering**
*For any* donor search with blood_group, radius_km, and eligible filters, all returned donors should match the blood group exactly, be within the specified radius from the hospital location (using haversine distance), and have eligible=true if the eligible filter is set.
**Validates: Requirements 6.1, 6.2, 6.3**

**Property 12: Donor registration completeness**
*For any* donor registration with all required fields, the persisted donor record should contain all provided values (name, phone, email, blood_group, last_donation_date, eligible, location_lat, location_lon) unchanged.
**Validates: Requirements 6.4**

**Property 13: Donor eligibility calculation**
*For any* donor with a last_donation_date, the eligible status should be true if and only if (current_date - last_donation_date) > 90 days.
**Validates: Requirements 6.5**

**Property 14: Notification message generation**
*For any* donor notification with hospital context, the generated message should match the template format "Urgent! {hospital_name} needs {blood_group} donors. If eligible, please contact {phone} or click {link}." with all placeholders replaced by actual values.
**Validates: Requirements 7.1, 7.2**

**Property 15: Notification logging**
*For any* notification sent or simulated, an audit log entry should be created containing donor_id, template_id, message content, status, and timestamp.
**Validates: Requirements 7.3**

**Property 16: Role-based access control**
*For any* user with role 'staff', access should be granted to inventory management, donor management, and read-only forecasts, and denied to transfer approvals and settings; for any user with role 'admin', access should be granted to all features.
**Validates: Requirements 9.1, 9.2, 9.3**

**Property 17: Audit logging for sensitive actions**
*For any* transfer approval or notification action, an audit log entry should be created with user_id, action type, resource_id, and timestamp before the action is executed.
**Validates: Requirements 9.4**

**Property 18: Donor data encryption**
*For any* donor record persisted to the database, the phone and email fields should be encrypted such that the stored values differ from the plaintext inputs, and decryption should recover the original values.
**Validates: Requirements 9.5**

**Property 19: Training data preprocessing**
*For any* historical usage dataset with gaps, the preprocessing pipeline should produce a continuous daily series where missing dates are filled with zero units, and the aggregated daily totals match the original data.
**Validates: Requirements 10.1**

**Property 20: Train-test split**
*For any* historical dataset with N days of data where N > 30, the test set should contain the last 30 days and the training set should contain the first (N - 30) days, with no overlap.
**Validates: Requirements 10.2**

**Property 21: Model evaluation metrics**
*For any* set of predictions and actual values, MAE should equal the mean of absolute differences, and MAPE should equal the mean of (|actual - predicted| / actual) * 100, excluding cases where actual = 0.
**Validates: Requirements 10.3**

**Property 22: Forecast API response structure**
*For any* forecast API call, the JSON response should contain fields: hospital_id, blood_group, component, forecast (array of objects with date, predicted, lower, upper), and generated_at timestamp.
**Validates: Requirements 10.5**

**Property 23: Error logging completeness**
*For any* error during CSV parsing or API request, a log entry should be created containing timestamp, error type, error message, and relevant context (file name for CSV errors, request details for API errors).
**Validates: Requirements 11.1, 11.5**

**Property 24: Forecast job logging**
*For any* execution of the daily forecast job, a log entry should be created containing job_start_time, job_end_time, and count of forecasts generated.
**Validates: Requirements 11.2**

**Property 25: Model drift calculation**
*For any* week of forecast and actual usage data, the drift metric should equal the mean absolute percentage error between forecasted and actual values for that week.
**Validates: Requirements 11.3, 11.4**

**Property 26: Configuration loading**
*For any* external service configuration (SMS gateway API key, database URL), when the application starts, the configuration value should be loaded from environment variables, and if missing, the application should log a warning or fail to start based on whether the service is required.
**Validates: Requirements 12.4**

## Error Handling

### Error Categories

**1. Validation Errors (400 Bad Request)**
- Invalid CSV format
- Invalid blood group values
- Duplicate record IDs
- Missing required fields
- Invalid date formats
- Negative or zero units

**2. Authorization Errors (401/403)**
- Invalid credentials
- Insufficient permissions
- Expired session tokens

**3. Not Found Errors (404)**
- Hospital not found
- Donor not found
- Transfer not found
- Forecast not available

**4. Business Logic Errors (422 Unprocessable Entity)**
- Cannot approve already approved transfer
- Cannot register donor with future last_donation_date
- Cannot create forecast with insufficient historical data

**5. External Service Errors (502/503)**
- e-RaktKosh API unavailable
- SMS gateway timeout
- Database connection failure

**6. Internal Errors (500)**
- Model training failure
- Unexpected calculation errors
- Database constraint violations

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_BLOOD_GROUP",
    "message": "Blood group 'XYZ' is not recognized",
    "details": {
      "field": "blood_group",
      "value": "XYZ",
      "accepted_values": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    },
    "timestamp": "2025-11-27T10:30:00Z"
  }
}
```

### Error Handling Strategies

**Graceful Degradation:**
- If e-RaktKosh API is unavailable, continue with manual entry and CSV upload
- If SMS gateway fails, fall back to in-app notifications and email
- If forecast generation fails for one hospital, continue with others and log the failure

**Retry Logic:**
- External API calls: 3 retries with exponential backoff
- Database transactions: 2 retries for deadlock/timeout errors
- Background jobs: Retry failed jobs after 5 minutes

**Logging:**
- All errors logged with full stack trace
- Sensitive data (passwords, API keys) redacted from logs
- Error logs include request ID for tracing

**User Feedback:**
- Clear, actionable error messages
- Suggestions for resolution when possible
- Contact information for support

## Testing Strategy

### Unit Testing

**Framework:** pytest with pytest-cov for coverage

**Unit Test Coverage:**
- Data validation functions (blood group normalization, date parsing)
- Calculation functions (expiry risk, urgency score, ETA, distance)
- Filtering and aggregation logic
- Template rendering
- Encryption/decryption functions

**Example Unit Tests:**
```python
def test_normalize_blood_group_variations():
    assert normalize_blood_group("A+") == "A+"
    assert normalize_blood_group("A Positive") == "A+"
    assert normalize_blood_group("a+") == "A+"
    with pytest.raises(ValueError):
        normalize_blood_group("XYZ")

def test_calculate_expiry_risk():
    record = InventoryRecord(
        record_id="R1",
        hospital_id="H1",
        blood_group="A+",
        component="RBC",
        units=5,
        unit_expiry_date=date.today() + timedelta(days=2),
        collection_date=date.today() - timedelta(days=30)
    )
    risk = calculate_expiry_risk(record)
    expected = (1 / (2 + 1)) * 5
    assert abs(risk - expected) < 0.01

def test_haversine_distance():
    # Mumbai to Pune (approx 150 km)
    lat1, lon1 = 19.0760, 72.8777
    lat2, lon2 = 18.5204, 73.8567
    distance = haversine_distance(lat1, lon1, lat2, lon2)
    assert 145 < distance < 155
```

### Property-Based Testing

**Framework:** Hypothesis (Python property-based testing library)

**Configuration:**
- Minimum 100 iterations per property test
- Shrinking enabled to find minimal failing examples
- Seed for reproducibility in CI/CD

**Property Test Implementation:**

Each property test must:
1. Be tagged with a comment referencing the design document property
2. Use Hypothesis strategies to generate random test data
3. Verify the property holds for all generated inputs
4. Include edge cases in the generation strategy

**Example Property Tests:**

```python
from hypothesis import given, strategies as st
from hypothesis.strategies import composite

@composite
def inventory_record_strategy(draw):
    """Generate random inventory records"""
    return InventoryRecord(
        record_id=draw(st.text(min_size=1, max_size=50)),
        hospital_id=draw(st.sampled_from(["H1", "H2", "H3"])),
        blood_group=draw(st.sampled_from(list(BloodGroup))),
        component=draw(st.sampled_from(list(Component))),
        units=draw(st.integers(min_value=1, max_value=100)),
        unit_expiry_date=draw(st.dates(
            min_value=date.today(),
            max_value=date.today() + timedelta(days=365)
        )),
        collection_date=draw(st.dates(
            min_value=date.today() - timedelta(days=365),
            max_value=date.today()
        ))
    )

# **Feature: smart-blood-bank, Property 6: Expiry risk calculation**
@given(record=inventory_record_strategy())
def test_property_expiry_risk_calculation(record):
    """
    For any inventory record, the expiry risk score should equal
    (1 / (days_to_expiry + 1)) * units
    """
    risk_score = calculate_expiry_risk(record)
    days_to_expiry = (record.unit_expiry_date - date.today()).days
    expected_score = (1 / (days_to_expiry + 1)) * record.units
    assert abs(risk_score - expected_score) < 0.01

# **Feature: smart-blood-bank, Property 3: Inventory filtering composition**
@given(
    records=st.lists(inventory_record_strategy(), min_size=10, max_size=100),
    hospital_filter=st.sampled_from(["H1", "H2", "H3", None]),
    blood_group_filter=st.sampled_from(list(BloodGroup) + [None]),
    component_filter=st.sampled_from(list(Component) + [None])
)
def test_property_filter_composition(records, hospital_filter, blood_group_filter, component_filter):
    """
    For any combination of filters, the result should match all criteria
    and be equivalent to applying filters in any order
    """
    filters = InventoryFilters(
        hospital_id=hospital_filter,
        blood_group=blood_group_filter,
        component=component_filter
    )
    
    result = filter_inventory(records, filters)
    
    # Verify all results match filters
    for record in result:
        if hospital_filter:
            assert record.hospital_id == hospital_filter
        if blood_group_filter:
            assert record.blood_group == blood_group_filter
        if component_filter:
            assert record.component == component_filter
    
    # Verify order independence
    result_alt = records
    if hospital_filter:
        result_alt = [r for r in result_alt if r.hospital_id == hospital_filter]
    if blood_group_filter:
        result_alt = [r for r in result_alt if r.blood_group == blood_group_filter]
    if component_filter:
        result_alt = [r for r in result_alt if r.component == component_filter]
    
    assert set(r.record_id for r in result) == set(r.record_id for r in result_alt)

# **Feature: smart-blood-bank, Property 10: Transfer approval inventory update**
@given(
    source_inventory=st.integers(min_value=10, max_value=100),
    dest_inventory=st.integers(min_value=0, max_value=100),
    transfer_units=st.integers(min_value=1, max_value=10)
)
def test_property_transfer_inventory_update(source_inventory, dest_inventory, transfer_units):
    """
    For any approved transfer, source inventory should decrease by N
    and destination inventory should increase by N
    """
    # Setup
    source_before = source_inventory
    dest_before = dest_inventory
    
    # Execute transfer
    transfer = Transfer(
        source_hospital_id="H1",
        destination_hospital_id="H2",
        blood_group="A+",
        component="RBC",
        units=transfer_units
    )
    
    source_after, dest_after = execute_transfer(transfer, source_before, dest_before)
    
    # Verify
    assert source_after == source_before - transfer_units
    assert dest_after == dest_before + transfer_units
    assert source_after + dest_after == source_before + dest_before  # Conservation
```

### Integration Testing

**Scope:**
- API endpoint testing with test database
- End-to-end workflows (upload CSV → view inventory → generate forecast → approve transfer)
- External service mocking (e-RaktKosh, SMS gateway)

**Tools:**
- pytest with FastAPI TestClient
- Docker Compose for test database
- responses library for HTTP mocking

**Example Integration Tests:**
```python
def test_csv_upload_workflow(test_client, test_db):
    # Upload CSV
    with open("test_data/inventory.csv", "rb") as f:
        response = test_client.post("/api/upload/inventory", files={"file": f})
    assert response.status_code == 200
    
    # Verify records in database
    inventory = test_client.get("/api/inventory?hospital_id=H1")
    assert len(inventory.json()) > 0

def test_forecast_generation_workflow(test_client, test_db, seed_usage_data):
    # Generate forecast
    response = test_client.get("/api/forecast?hospital_id=H1&days=7")
    assert response.status_code == 200
    
    forecast = response.json()
    assert len(forecast["forecast"]) == 7
    assert all("predicted" in point for point in forecast["forecast"])
```

### Performance Testing

**Metrics:**
- API response time < 500ms for 95th percentile
- Forecast generation < 5 seconds per hospital/blood group
- CSV upload processing < 10 seconds for 10,000 records
- Database queries < 100ms for filtered inventory

**Tools:**
- Locust for load testing
- pytest-benchmark for micro-benchmarks

### Security Testing

**Checks:**
- SQL injection prevention (parameterized queries)
- XSS prevention (input sanitization)
- CSRF protection (tokens)
- Authentication bypass attempts
- Authorization boundary testing
- Encryption verification for sensitive data

### Test Data Management

**Seed Data:**
- 3 hospitals within 30km (Mumbai, Thane, Navi Mumbai)
- 6 months of daily usage data (180 days)
- All 8 blood groups × 3 components = 24 combinations per hospital
- 100 registered donors with varied eligibility
- 50 historical transfers

**Data Generation:**
- Faker library for realistic names, addresses, phone numbers
- Random but realistic usage patterns (higher on weekdays, spikes for emergencies)
- Seasonal variations in demand

## Deployment Architecture

### Docker Configuration

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run database migrations
RUN alembic upgrade head

# Expose port
EXPOSE 8000

# Start application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "app.main:app", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:14-alpine
    environment:
      POSTGRES_DB: bloodbank
      POSTGRES_USER: bloodbank
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: .
    environment:
      DATABASE_URL: postgresql://bloodbank:${DB_PASSWORD}@db:5432/bloodbank
      SMS_API_KEY: ${SMS_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    depends_on:
      - db
    volumes:
      - ./logs:/app/logs

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bloodbank

# Security
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# External Services
ERAKTKOSH_API_URL=https://api.eraktkosh.in
ERAKTKOSH_API_KEY=your-api-key
SMS_GATEWAY_URL=https://api.twilio.com
SMS_API_KEY=your-twilio-key
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your-email
EMAIL_PASSWORD=your-password

# Application Config
EXPIRY_THRESHOLD_DAYS=3
TRANSFER_RADIUS_KM=50
FORECAST_HORIZON_DAYS=7
DONOR_ELIGIBILITY_DAYS=90

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/bloodbank.log
```

### Cloud Deployment

**Heroku:**
```bash
# Create app
heroku create smart-blood-bank

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=xxx SMS_API_KEY=xxx

# Deploy
git push heroku main

# Run migrations
heroku run alembic upgrade head

# Seed data
heroku run python scripts/seed_data.py
```

**Render:**
- Create Blueprint with web service + PostgreSQL
- Configure environment variables in dashboard
- Auto-deploy from GitHub repository

**Railway:**
- Connect GitHub repository
- Add PostgreSQL plugin
- Configure environment variables
- Deploy with one click

### Monitoring and Observability

**Logging:**
- Structured JSON logs
- Log aggregation with CloudWatch/Papertrail
- Error tracking with Sentry

**Metrics:**
- Application metrics (request rate, latency, error rate)
- Business metrics (forecasts generated, transfers approved, donors notified)
- Infrastructure metrics (CPU, memory, database connections)

**Alerting:**
- High error rate (> 5% of requests)
- Forecast job failures
- Database connection pool exhaustion
- API response time > 2 seconds

### Backup and Recovery

**Database Backups:**
- Automated daily backups
- Point-in-time recovery capability
- Backup retention: 30 days

**Disaster Recovery:**
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 24 hours
- Documented recovery procedures

## Security Considerations

### Data Protection

**Encryption:**
- Data at rest: PostgreSQL encryption
- Data in transit: TLS 1.3
- Sensitive fields: AES-256 encryption for donor contact info

**Access Control:**
- Role-based access control (RBAC)
- Principle of least privilege
- Session management with JWT tokens
- Token expiration and refresh

### Compliance

**Data Privacy:**
- No patient-identifiable information stored
- Donor consent for contact information
- Right to deletion (GDPR compliance)
- Data retention policies

**Audit Trail:**
- All sensitive actions logged
- Immutable audit logs
- Regular audit log reviews

### API Security

**Authentication:**
- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting (100 requests/minute per user)

**Input Validation:**
- Pydantic models for request validation
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CSRF protection

**API Keys:**
- Stored in environment variables
- Rotated regularly
- Never logged or exposed in responses

## Performance Optimization

### Database Optimization

**Indexing Strategy:**
- Indexes on frequently queried columns (hospital_id, blood_group, usage_date)
- Composite indexes for multi-column filters
- Partial indexes for filtered queries (e.g., eligible donors)

**Query Optimization:**
- Use of EXPLAIN ANALYZE for slow queries
- Connection pooling (max 20 connections)
- Query result caching for forecasts (1 hour TTL)

### Application Optimization

**Caching:**
- Redis for forecast results (1 hour TTL)
- Hospital location data (24 hour TTL)
- Static configuration (infinite TTL)

**Async Processing:**
- Background jobs for forecast generation
- Async notification sending
- Batch processing for bulk operations

**Frontend Optimization:**
- Code splitting and lazy loading
- Image optimization and compression
- Minification and bundling
- CDN for static assets

### Scalability

**Horizontal Scaling:**
- Stateless application servers
- Load balancer (Nginx/AWS ALB)
- Database read replicas for queries

**Vertical Scaling:**
- Increase server resources as needed
- Database connection pool tuning
- Worker process optimization

## Future Enhancements

### Phase 2 Features

1. **Advanced ML Models:**
   - LSTM for better long-term forecasting
   - Anomaly detection for unusual demand patterns
   - Multi-variate models incorporating external factors (weather, events)

2. **Mobile Application:**
   - Native iOS/Android apps for staff
   - Donor mobile app for self-service
   - Push notifications

3. **Real-time Updates:**
   - WebSocket connections for live inventory updates
   - Real-time transfer tracking
   - Live dashboard updates

4. **Advanced Analytics:**
   - Wastage analysis and reduction recommendations
   - Donor retention analytics
   - Hospital performance benchmarking

5. **Integration Enhancements:**
   - Bi-directional e-RaktKosh sync
   - Integration with hospital EMR systems
   - Automated ordering from blood banks

### Technical Debt

- Migrate from Streamlit to React for production UI
- Implement comprehensive API documentation (OpenAPI/Swagger)
- Add GraphQL API for flexible querying
- Implement event sourcing for audit trail
- Add multi-tenancy support for different regions
