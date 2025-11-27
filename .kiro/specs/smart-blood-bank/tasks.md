# Implementation Plan

- [x] 1. Set up project structure and development environment





  - Create directory structure: backend (app/models, app/services, app/api, app/repositories), frontend, tests, scripts, docker
  - Initialize Python project with requirements.txt (FastAPI, SQLAlchemy, Alembic, Prophet, Pandas, Hypothesis, pytest)
  - Set up PostgreSQL database with Docker Compose
  - Configure Alembic for database migrations
  - Create .env.example with all required environment variables
  - _Requirements: 12.1, 12.2_

- [x] 2. Implement database schema and models




  - [x] 2.1 Create database migration for all tables


    - Write Alembic migration for hospitals, inventory, usage, donors, forecasts, transfers, audit_logs, users, notifications tables
    - Add indexes for common query patterns
    - Add constraints and checks as defined in schema
    - _Requirements: 1.1, 2.1, 6.4, 9.4_
  - [x] 2.2 Create SQLAlchemy ORM models


    - Implement model classes for all database tables
    - Add relationships between models
    - _Requirements: 1.1, 2.1, 6.4_
  - [x] 2.3 Create Pydantic schemas for API validation


    - Implement request/response schemas for all endpoints
    - Add validators for blood groups, dates, and units
    - _Requirements: 1.1, 1.2_
  - [ ]* 2.4 Write property test for blood group normalization
    - **Property 2: Blood group normalization**
    - **Validates: Requirements 1.2**

- [x] 3. Implement data ingestion layer





  - [x] 3.1 Create CSV validation and parsing service


    - Implement CSV format validation
    - Add blood group normalization function
    - Add duplicate detection logic
    - _Requirements: 1.1, 1.2, 1.3_
  - [ ]* 3.2 Write property test for CSV validation and import
    - **Property 1: CSV validation and import**
    - **Validates: Requirements 1.1, 1.2, 1.3**
  - [x] 3.3 Create inventory repository with CRUD operations


    - Implement repository pattern for inventory table
    - Add methods for create, read, update, delete operations
    - _Requirements: 1.1, 1.4, 2.1_
  - [x] 3.4 Implement CSV upload API endpoint


    - Create POST /api/upload/inventory endpoint
    - Handle file upload and validation
    - Return success/error response with details
    - _Requirements: 1.1_
  - [x] 3.5 Implement manual inventory entry API endpoint


    - Create POST /api/inventory endpoint
    - Validate and store inventory record
    - _Requirements: 1.4_
  - [ ]* 3.6 Write integration test for CSV upload workflow
    - Test end-to-end CSV upload with valid and invalid data
    - _Requirements: 1.1, 1.2, 1.3_

- [x] 4. Implement inventory management features


  - [x] 4.1 Create inventory filtering service


    - Implement multi-criteria filtering logic
    - Support hospital_id, blood_group, component filters
    - _Requirements: 2.2, 2.3, 2.4, 2.5_
  - [ ]* 4.2 Write property test for inventory filtering composition
    - **Property 3: Inventory filtering composition**
    - **Validates: Requirements 2.2, 2.3, 2.4, 2.5**
  - [x] 4.3 Implement inventory query API endpoints


    - Create GET /api/inventory endpoint with filter parameters
    - Create GET /api/hospitals endpoint
    - Return paginated results
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ]* 4.4 Write unit tests for inventory filtering
    - Test individual filter types
    - Test filter combinations
    - _Requirements: 2.2, 2.3, 2.4, 2.5_

- [x] 5. Implement expiry risk calculation


  - [x] 5.1 Create expiry risk service


    - Implement days_to_expiry calculation
    - Implement expiry_risk_score formula
    - Add high-risk flagging logic with configurable threshold
    - _Requirements: 4.1, 4.2, 4.3, 4.5_
  - [ ]* 5.2 Write property test for expiry risk calculation
    - **Property 6: Expiry risk calculation**
    - **Validates: Requirements 4.1, 4.2, 4.3**
  - [x] 5.3 Add expiry summary to dashboard API


    - Create GET /api/dashboard/summary endpoint
    - Include total units, units near expiry, high-risk count
    - _Requirements: 4.4_
  - [ ]* 5.4 Write unit tests for expiry risk edge cases
    - Test with expiry dates today, tomorrow, past dates
    - Test threshold boundary conditions
    - _Requirements: 4.1, 4.2, 4.3_

- [x] 6. Implement forecasting engine


  - [x] 6.1 Create usage data repository and aggregation service


    - Implement repository for usage table
    - Add daily aggregation by hospital, blood group, component
    - _Requirements: 3.5, 10.1_
  - [ ]* 6.2 Write property test for historical data aggregation
    - **Property 5: Historical data aggregation**
    - **Validates: Requirements 3.5**
  - [x] 6.3 Implement data preprocessing pipeline


    - Fill missing dates with zero units
    - Create continuous daily time series
    - _Requirements: 10.1_
  - [ ]* 6.4 Write property test for training data preprocessing
    - **Property 19: Training data preprocessing**
    - **Validates: Requirements 10.1**
  - [x] 6.5 Implement train-test split logic

    - Split data into last 30 days (test) and earlier (train)
    - _Requirements: 10.2_
  - [ ]* 6.6 Write property test for train-test split
    - **Property 20: Train-test split**
    - **Validates: Requirements 10.2**
  - [x] 6.7 Implement Prophet model training and prediction

    - Configure Prophet with weekly seasonality
    - Train model on historical data
    - Generate forecasts with confidence intervals
    - _Requirements: 3.1, 3.2, 10.4_
  - [x] 6.8 Implement model evaluation metrics

    - Calculate MAE and MAPE on test set
    - _Requirements: 10.3_
  - [ ]* 6.9 Write property test for model evaluation metrics
    - **Property 21: Model evaluation metrics**
    - **Validates: Requirements 10.3**
  - [x] 6.10 Create forecast repository for storing predictions

    - Implement repository for forecasts table
    - Add methods to store and retrieve forecasts
    - _Requirements: 3.1, 3.2_
  - [x] 6.11 Implement forecast generation service

    - Orchestrate data loading, preprocessing, training, prediction
    - Store forecasts in database
    - _Requirements: 3.1, 3.2, 10.4_
  - [ ]* 6.12 Write property test for forecast generation structure
    - **Property 4: Forecast generation structure**
    - **Validates: Requirements 3.1, 3.2, 3.3, 3.4**
  - [x] 6.13 Create forecast API endpoint


    - Implement GET /api/forecast endpoint with hospital_id and days parameters
    - Return forecast with confidence intervals
    - _Requirements: 3.1, 3.2, 10.5_
  - [ ]* 6.14 Write property test for forecast API response structure
    - **Property 22: Forecast API response structure**
    - **Validates: Requirements 10.5**
  - [ ]* 6.15 Write integration test for forecast generation workflow
    - Test end-to-end forecast generation with seed data
    - _Requirements: 3.1, 3.2, 10.4_

- [x] 7. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.

- [x] 8. Implement transfer recommendation engine



  - [x] 8.1 Create geospatial utilities

    - Implement haversine distance calculation
    - Add function to find hospitals within radius
    - _Requirements: 5.2_
  - [ ]* 8.2 Write unit tests for distance calculations
    - Test haversine formula with known coordinates
    - _Requirements: 5.2_
  - [x] 8.3 Implement deficit and surplus calculation

    - Calculate deficit as forecast - inventory
    - Calculate surplus as inventory - forecast
    - Filter by thresholds
    - _Requirements: 5.1, 5.2_
  - [ ]* 8.4 Write property test for deficit and surplus calculation
    - **Property 7: Deficit and surplus calculation**
    - **Validates: Requirements 5.1, 5.2**
  - [x] 8.5 Implement transfer urgency scoring algorithm

    - Normalize expiry, distance, and surplus values
    - Calculate weighted score with configurable weights
    - _Requirements: 5.3, 5.4_
  - [ ]* 8.6 Write property test for transfer urgency scoring
    - **Property 8: Transfer urgency scoring**
    - **Validates: Requirements 5.3, 5.4**
  - [x] 8.7 Implement ETA calculation

    - Calculate ETA as distance / 40 km/h
    - _Requirements: 5.5_
  - [ ]* 8.8 Write property test for transfer ETA calculation
    - **Property 9: Transfer ETA calculation**
    - **Validates: Requirements 5.5**
  - [x] 8.9 Create transfer recommendation service

    - Orchestrate deficit calculation, candidate finding, scoring, ranking
    - Generate top N recommendations
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_
  - [x] 8.10 Create transfer repository

    - Implement repository for transfers table
    - Add methods for CRUD operations
    - _Requirements: 5.7_
  - [x] 8.11 Implement transfer API endpoints

    - Create GET /api/transfers endpoint with optional hospital_id filter
    - Create POST /api/transfers/approve endpoint
    - _Requirements: 5.6, 5.7_
  - [x] 8.12 Implement transfer approval logic with inventory updates

    - Update source hospital inventory (decrease)
    - Update destination hospital inventory (increase)
    - Record transfer in database
    - _Requirements: 5.7_
  - [ ]* 8.13 Write property test for transfer approval inventory update
    - **Property 10: Transfer approval inventory update**
    - **Validates: Requirements 5.7**
  - [ ]* 8.14 Write integration test for transfer workflow
    - Test recommendation generation and approval
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7_

- [x] 9. Implement donor management


  - [x] 9.1 Create donor repository


    - Implement repository for donors table
    - Add CRUD operations
    - _Requirements: 6.4_
  - [x] 9.2 Implement donor eligibility calculation

    - Calculate eligibility based on 90-day rule
    - _Requirements: 6.5_
  - [ ]* 9.3 Write property test for donor eligibility calculation
    - **Property 13: Donor eligibility calculation**
    - **Validates: Requirements 6.5**
  - [x] 9.4 Implement donor search service with filters


    - Filter by blood group
    - Filter by radius using geospatial query
    - Filter by eligibility status
    - _Requirements: 6.1, 6.2, 6.3_
  - [ ]* 9.5 Write property test for donor search filtering
    - **Property 11: Donor search filtering**
    - **Validates: Requirements 6.1, 6.2, 6.3**
  - [x] 9.6 Implement donor registration with encryption

    - Encrypt phone and email fields before storage
    - _Requirements: 6.4, 9.5_
  - [ ]* 9.7 Write property test for donor registration completeness
    - **Property 12: Donor registration completeness**
    - **Validates: Requirements 6.4**
  - [ ]* 9.8 Write property test for donor data encryption
    - **Property 18: Donor data encryption**
    - **Validates: Requirements 9.5**
  - [x] 9.9 Create donor API endpoints


    - Implement POST /api/donors (registration)
    - Implement GET /api/donors/search with filter parameters
    - _Requirements: 6.1, 6.2, 6.3, 6.4_
  - [ ]* 9.10 Write unit tests for donor management
    - Test registration validation
    - Test search with various filter combinations
    - _Requirements: 6.1, 6.2, 6.3, 6.4_

- [x] 10. Implement notification system


  - [x] 10.1 Create notification templates

    - Define SMS template with placeholders
    - Define email template
    - _Requirements: 7.2_
  - [x] 10.2 Implement message generation service

    - Replace template placeholders with actual values
    - _Requirements: 7.1, 7.2_
  - [ ]* 10.3 Write property test for notification message generation
    - **Property 14: Notification message generation**
    - **Validates: Requirements 7.1, 7.2**
  - [x] 10.4 Create notification repository

    - Implement repository for notifications table
    - Add logging methods
    - _Requirements: 7.3_
  - [x] 10.5 Implement SMS gateway integration with fallback

    - Integrate with Twilio or AWS SNS
    - Implement simulation mode when gateway unavailable
    - _Requirements: 7.4, 7.5_
  - [x] 10.6 Implement notification logging

    - Log all notifications with donor_id, template_id, status, timestamp
    - _Requirements: 7.3_
  - [ ]* 10.7 Write property test for notification logging
    - **Property 15: Notification logging**
    - **Validates: Requirements 7.3**
  - [x] 10.8 Create notification API endpoint

    - Implement POST /api/notify/donor endpoint
    - Handle both real and simulated sends
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_
  - [ ]* 10.9 Write integration test for notification workflow
    - Test message generation, sending, and logging
    - _Requirements: 7.1, 7.2, 7.3_

- [x] 11. Implement authentication and authorization



  - [x] 11.1 Create user repository

    - Implement repository for users table
    - Add authentication methods
    - _Requirements: 9.1, 9.2_
  - [x] 11.2 Implement password hashing with bcrypt

    - Hash passwords before storage
    - Verify passwords during login
    - _Requirements: 9.1, 9.2_
  - [x] 11.3 Implement JWT token generation and validation

    - Generate tokens on successful login
    - Validate tokens on protected endpoints
    - _Requirements: 9.1, 9.2_
  - [x] 11.4 Create authentication middleware

    - Extract and validate JWT from request headers
    - Attach user to request context
    - _Requirements: 9.1, 9.2_
  - [x] 11.5 Implement role-based access control

    - Define permissions for staff and admin roles
    - Check permissions before allowing actions
    - _Requirements: 9.1, 9.2, 9.3_
  - [ ]* 11.6 Write property test for role-based access control
    - **Property 16: Role-based access control**
    - **Validates: Requirements 9.1, 9.2, 9.3**
  - [x] 11.7 Create audit logging service

    - Log sensitive actions with user_id, action, resource, timestamp
    - _Requirements: 9.4_
  - [ ]* 11.8 Write property test for audit logging
    - **Property 17: Audit logging for sensitive actions**
    - **Validates: Requirements 9.4**
  - [x] 11.9 Create authentication API endpoints

    - Implement POST /api/auth/login
    - Implement POST /api/auth/logout
    - Implement GET /api/auth/me
    - _Requirements: 9.1, 9.2_
  - [x] 11.10 Apply authentication and authorization to all protected endpoints

    - Add middleware to inventory, forecast, transfer, donor endpoints
    - Enforce role-based permissions
    - _Requirements: 9.1, 9.2, 9.3_
  - [ ]* 11.11 Write integration tests for authentication flow
    - Test login, token validation, protected endpoint access
    - _Requirements: 9.1, 9.2, 9.3_

- [x] 12. Checkpoint - Ensure all tests pass

  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Implement background jobs and monitoring


  - [x] 13.1 Set up APScheduler for background jobs

    - Configure scheduler with job store
    - _Requirements: 11.2_
  - [x] 13.2 Create daily forecast generation job

    - Schedule job to run daily
    - Generate forecasts for all hospitals and blood groups
    - _Requirements: 11.2_
  - [x] 13.3 Implement job logging

    - Log job start, completion, and forecast count
    - _Requirements: 11.2_
  - [ ]* 13.4 Write property test for forecast job logging
    - **Property 24: Forecast job logging**
    - **Validates: Requirements 11.2**
  - [x] 13.5 Implement error logging service

    - Log CSV parsing errors with context
    - Log API errors with request details
    - _Requirements: 11.1, 11.5_
  - [ ]* 13.6 Write property test for error logging completeness
    - **Property 23: Error logging completeness**
    - **Validates: Requirements 11.1, 11.5**
  - [x] 13.7 Implement model drift monitoring

    - Calculate weekly MAPE between forecasts and actuals
    - _Requirements: 11.3, 11.4_
  - [ ]* 13.8 Write property test for model drift calculation
    - **Property 25: Model drift calculation**
    - **Validates: Requirements 11.3, 11.4**
  - [x] 13.9 Add drift metric to dashboard API

    - Include drift metric in GET /api/dashboard/summary
    - _Requirements: 11.4_
  - [ ]* 13.10 Write unit tests for background jobs
    - Test job scheduling and execution
    - _Requirements: 11.2_

- [x] 14. Implement frontend UI (Streamlit MVP)

  - [x] 14.1 Create Streamlit app structure

    - Set up main app with navigation sidebar
    - Create pages for Dashboard, Inventory, Forecasts, Transfers, Donors, Settings, Logs
    - _Requirements: 8.1_
  - [x] 14.2 Implement Dashboard page

    - Display KPIs: total units, units near expiry, predicted shortages, suggested transfers
    - Add refresh button
    - _Requirements: 8.2_
  - [x] 14.3 Implement Inventory page

    - Add CSV upload widget
    - Add manual entry form
    - Display inventory table with filters
    - _Requirements: 1.1, 1.4, 2.1, 2.2, 2.3, 2.4, 2.5_
  - [x] 14.4 Implement Forecasts page

    - Add hospital and blood group selectors
    - Display 7-day and 30-day forecast charts with confidence intervals
    - Use Plotly or Altair for interactive charts
    - _Requirements: 3.1, 3.2, 3.3, 3.4_
  - [x] 14.5 Implement Transfers page

    - Display recommended transfers table sorted by urgency
    - Add approve transfer button for each recommendation
    - Show distance and ETA
    - _Requirements: 5.6, 5.7_
  - [x] 14.6 Implement Donors page

    - Add donor registration form
    - Add donor search with filters
    - Display eligible donors table
    - Add notify donor button
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 7.1_
  - [x] 14.7 Implement map view for nearby hospitals

    - Use Folium or Pydeck for map visualization
    - Display hospital markers with names and distances
    - _Requirements: 8.4_
  - [x] 14.8 Optimize for low-bandwidth

    - Minimize data loading
    - Use caching for static data
    - Compress images
    - _Requirements: 8.3_
  - [x] 14.9 Implement Settings page

    - Add configuration forms for thresholds and weights
    - _Requirements: 4.5, 5.4_
  - [x] 14.10 Implement Logs page

    - Display audit logs and error logs
    - Add filtering by date and action type
    - _Requirements: 9.4, 11.1, 11.5_

- [x] 15. Create seed data and demo dataset


  - [x] 15.1 Create seed data script

    - Generate 3 hospitals within 30km (Mumbai, Thane, Navi Mumbai)
    - Generate 6 months of daily usage data for all blood groups and components
    - Generate 100 donors with varied eligibility
    - Generate 50 historical transfers
    - _Requirements: 12.5_
  - [x] 15.2 Create CSV templates

    - Create template files for hospitals.csv, inventory.csv, usage.csv, donors.csv
    - Include example data and column descriptions
    - _Requirements: 1.1, 12.5_
  - [x] 15.3 Implement database seeding command

    - Create script to load seed data into database
    - Add command to run from CLI
    - _Requirements: 12.5_

- [x] 16. Implement configuration and environment management

  - [x] 16.1 Create configuration loader

    - Load all settings from environment variables
    - Provide defaults for optional settings
    - _Requirements: 12.4_
  - [ ]* 16.2 Write property test for configuration loading
    - **Property 26: Configuration loading**
    - **Validates: Requirements 12.4**
  - [x] 16.3 Create .env.example file

    - Document all required and optional environment variables
    - _Requirements: 12.2_
  - [ ]* 16.4 Write unit tests for configuration validation
    - Test missing required variables
    - Test default values
    - _Requirements: 12.4_

- [x] 17. Create deployment artifacts

  - [x] 17.1 Create Dockerfile

    - Include Python dependencies, application code, migrations
    - Configure gunicorn with uvicorn workers
    - _Requirements: 12.1_
  - [x] 17.2 Create docker-compose.yml

    - Define services for database, backend, frontend
    - Configure environment variables and volumes
    - _Requirements: 12.1_
  - [x] 17.3 Write deployment documentation

    - Document local development setup steps
    - Document Heroku deployment steps
    - Document Render deployment steps
    - Document Railway deployment steps
    - _Requirements: 12.2, 12.3_
  - [x] 17.4 Create deployment scripts

    - Create script for Heroku deployment
    - Create script for database migration
    - Create script for seed data loading
    - _Requirements: 12.3_

- [x] 18. Final testing and documentation

  - [ ]* 18.1 Run full test suite
    - Execute all unit tests, property tests, and integration tests
    - Verify 80%+ code coverage
    - _Requirements: All_
  - [x] 18.2 Create README.md


    - Add project overview and features
    - Add installation instructions
    - Add usage guide
    - Add API documentation
    - Add deployment guide
    - _Requirements: 12.2_
  - [x] 18.3 Create API documentation

    - Document all endpoints with request/response examples
    - Use OpenAPI/Swagger specification
    - _Requirements: 12.2_
  - [ ]* 18.4 Perform end-to-end testing
    - Test complete workflows from UI
    - Verify all features work together
    - _Requirements: All_
  - [x] 18.5 Create demo screencast

    - Record 3-minute demo showing key features
    - Upload CSV, view inventory, generate forecast, approve transfer, notify donor
    - _Requirements: 12.2_

- [x] 19. Final Checkpoint - Ensure all tests pass


  - Ensure all tests pass, ask the user if questions arise.
