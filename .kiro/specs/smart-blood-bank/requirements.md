# Requirements Document

## Introduction

The Smart Blood Bank system is a lightweight, deployable web application designed for government hospital blood banks to optimize inventory management, forecast demand, and facilitate intelligent redistribution of blood products. The system ingests inventory data from multiple sources, provides demand forecasting using machine learning, identifies units at risk of expiry, recommends transfers between hospitals, and enables donor mobilization for predicted shortages. It integrates with e-RaktKosh as a read-only analytics layer where APIs are available.

## Glossary

- **Blood Bank System**: The complete web application for managing blood inventory, forecasting, and transfers
- **Hospital**: A government medical facility with a blood bank that uses the system
- **Blood Component**: One of three types of blood products: Red Blood Cells (RBC), Platelets, or Plasma
- **Blood Group**: One of the standard blood types (A+, A-, B+, B-, AB+, AB-, O+, O-)
- **Inventory Unit**: A single unit of a blood component with specific collection and expiry dates
- **Forecast Engine**: The machine learning component that predicts future blood demand
- **Transfer Recommendation Engine**: The algorithm that identifies optimal blood transfers between hospitals
- **Donor**: A registered individual eligible to donate blood
- **e-RaktKosh**: The government blood bank management system providing read-only API access
- **Expiry Risk Score**: A calculated value indicating likelihood of blood unit expiration before use
- **Transfer Urgency Score**: A weighted calculation combining expiry risk, distance, and surplus availability
- **Confidence Interval**: The statistical range within which forecasted demand is expected to fall
- **Staff User**: A hospital employee with access to inventory and donor management features
- **Admin User**: A system administrator with full access including transfer approvals and system settings

## Requirements

### Requirement 1

**User Story:** As a hospital staff member, I want to input inventory data through multiple methods, so that I can maintain accurate blood stock records regardless of data source availability.

#### Acceptance Criteria

1. WHEN a staff user uploads a CSV file with inventory data THEN the Blood Bank System SHALL validate the file format and import valid records into the database
2. WHEN the CSV contains invalid blood group values THEN the Blood Bank System SHALL normalize standard variations and reject unrecognizable values
3. WHEN the CSV contains duplicate record identifiers THEN the Blood Bank System SHALL reject the duplicates and log the rejection reason
4. WHEN a staff user submits the manual entry form with inventory details THEN the Blood Bank System SHALL create a new inventory record with the provided data
5. WHERE e-RaktKosh API is available, WHEN the system polls the API endpoint THEN the Blood Bank System SHALL ingest inventory data in read-only mode

### Requirement 2

**User Story:** As a hospital staff member, I want to view current inventory filtered by hospital, blood group, and component, so that I can quickly assess available stock levels.

#### Acceptance Criteria

1. WHEN a staff user accesses the inventory page THEN the Blood Bank System SHALL display all inventory records with hospital name, blood group, component, units, and expiry date
2. WHEN a staff user applies a hospital filter THEN the Blood Bank System SHALL display only inventory records matching the selected hospital identifier
3. WHEN a staff user applies a blood group filter THEN the Blood Bank System SHALL display only inventory records matching the selected blood group
4. WHEN a staff user applies a component filter THEN the Blood Bank System SHALL display only inventory records matching the selected component type
5. WHEN a staff user combines multiple filters THEN the Blood Bank System SHALL display only inventory records matching all selected criteria

### Requirement 3

**User Story:** As a hospital administrator, I want to see demand forecasts for the next 7 and 30 days per hospital and blood group, so that I can plan procurement and prevent shortages.

#### Acceptance Criteria

1. WHEN an admin user requests a 7-day forecast for a hospital and blood group THEN the Forecast Engine SHALL return predicted daily demand with confidence intervals
2. WHEN an admin user requests a 30-day forecast for a hospital and blood group THEN the Forecast Engine SHALL return predicted daily demand with confidence intervals
3. WHEN the Forecast Engine generates predictions THEN the Blood Bank System SHALL display the forecast as an interactive chart with date on x-axis and units on y-axis
4. WHEN the forecast is displayed THEN the Blood Bank System SHALL show upper and lower confidence bounds as shaded regions around the prediction line
5. WHEN the Forecast Engine processes historical usage data THEN the Blood Bank System SHALL aggregate daily units issued by hospital, blood group, and component for the last 180 days

### Requirement 4

**User Story:** As a hospital administrator, I want to identify blood units at high risk of expiry, so that I can prioritize their use or transfer before they become unusable.

#### Acceptance Criteria

1. WHEN the system calculates expiry risk THEN the Blood Bank System SHALL compute days to expiry as the difference between current date and unit expiry date
2. WHEN days to expiry is computed THEN the Blood Bank System SHALL calculate expiry risk score as 1 divided by (days to expiry plus 1) multiplied by units
3. WHEN days to expiry is less than or equal to 3 days THEN the Blood Bank System SHALL flag the unit as high-risk
4. WHEN the dashboard loads THEN the Blood Bank System SHALL display the total count of units near expiry in the key performance indicators section
5. WHERE the expiry threshold is configurable, WHEN an admin user modifies the threshold value THEN the Blood Bank System SHALL apply the new threshold to all future expiry risk calculations

### Requirement 5

**User Story:** As a hospital administrator, I want to receive ranked transfer recommendations to nearby hospitals, so that I can redistribute surplus or expiring blood units efficiently.

#### Acceptance Criteria

1. WHEN the Transfer Recommendation Engine evaluates a hospital THEN the Blood Bank System SHALL compute deficit blood groups by subtracting current inventory from forecasted demand for the next configured days
2. WHEN deficit groups are identified THEN the Transfer Recommendation Engine SHALL query hospitals within a configured radius for surplus units where inventory minus forecast exceeds a threshold
3. WHEN candidate transfers are identified THEN the Transfer Recommendation Engine SHALL calculate transfer urgency score as weighted sum of normalized days to expiry, normalized distance, and normalized surplus
4. WHEN transfer urgency scores are calculated THEN the Blood Bank System SHALL apply default weights of 0.6 for expiry, 0.2 for distance, and 0.2 for surplus
5. WHEN transfer recommendations are generated THEN the Blood Bank System SHALL compute estimated time of arrival as distance divided by 40 kilometers per hour
6. WHEN the transfers page loads THEN the Blood Bank System SHALL display recommended transfers sorted by urgency score with hospital names, blood group, units, distance, and estimated time of arrival
7. WHEN an admin user clicks the approve transfer button THEN the Blood Bank System SHALL record the transfer approval and update inventory for both source and destination hospitals

### Requirement 6

**User Story:** As a hospital staff member, I want to search for eligible donors by blood group and location, so that I can mobilize donors when shortages are predicted.

#### Acceptance Criteria

1. WHEN a staff user searches for donors with a blood group filter THEN the Blood Bank System SHALL return only donors matching the specified blood group
2. WHEN a staff user searches for donors with a radius filter THEN the Blood Bank System SHALL return only donors within the specified distance from the hospital location
3. WHEN a staff user searches for donors with an eligible filter THEN the Blood Bank System SHALL return only donors where eligible boolean is true
4. WHEN a staff user registers a new donor THEN the Blood Bank System SHALL store the donor name, phone, email, blood group, last donation date, eligibility status, and location coordinates
5. WHEN the system evaluates donor eligibility THEN the Blood Bank System SHALL calculate eligibility based on last donation date being more than 90 days ago

### Requirement 7

**User Story:** As a hospital staff member, I want to trigger donor mobilization messages using templates, so that I can quickly notify eligible donors about urgent blood needs.

#### Acceptance Criteria

1. WHEN a staff user selects a donor and message template THEN the Blood Bank System SHALL generate a notification with hospital name, blood group, contact phone, and contact link
2. WHEN a notification is generated THEN the Blood Bank System SHALL populate the SMS template with format "Urgent! [Hospital name] needs [blood_group] donors. If eligible, please contact [phone] or click [link]."
3. WHEN a notification is sent THEN the Blood Bank System SHALL log the notification event with donor identifier, timestamp, and message template identifier
4. WHERE an SMS gateway is configured, WHEN a notification is triggered THEN the Blood Bank System SHALL send the message via the external SMS API
5. WHERE no SMS gateway is configured, WHEN a notification is triggered THEN the Blood Bank System SHALL simulate the send operation and display an in-app alert

### Requirement 8

**User Story:** As a hospital staff member, I want a simple navigation interface optimized for low-bandwidth connections, so that I can access all system features efficiently even with limited internet connectivity.

#### Acceptance Criteria

1. WHEN a user accesses the application THEN the Blood Bank System SHALL display a left navigation menu with links to Dashboard, Inventory, Forecasts, Transfers, Donors, Settings, and Logs
2. WHEN the dashboard loads THEN the Blood Bank System SHALL display key performance indicators for total units, units near expiry, predicted shortage groups, and suggested transfers
3. WHEN pages load THEN the Blood Bank System SHALL minimize asset sizes and use efficient rendering to support low-bandwidth connections
4. WHEN the map view loads THEN the Blood Bank System SHALL display nearby blood banks with hospital markers showing name and distance
5. WHEN a user navigates between pages THEN the Blood Bank System SHALL maintain responsive performance with page load times under 3 seconds on 2G connections

### Requirement 9

**User Story:** As a system administrator, I want role-based access control, so that I can ensure staff and admin users have appropriate permissions for their responsibilities.

#### Acceptance Criteria

1. WHEN a staff user logs in THEN the Blood Bank System SHALL grant access to inventory management, donor management, and view-only forecast features
2. WHEN an admin user logs in THEN the Blood Bank System SHALL grant access to all features including transfer approvals, system settings, and audit logs
3. WHEN a user attempts to access a restricted feature THEN the Blood Bank System SHALL deny access and display an authorization error message
4. WHEN any user performs a transfer approval or notification action THEN the Blood Bank System SHALL record the action in the audit log with user identifier, timestamp, and action details
5. WHERE donor contact information is stored, WHEN the data is persisted THEN the Blood Bank System SHALL encrypt the phone and email fields

### Requirement 10

**User Story:** As a system administrator, I want the forecast model to be trained and evaluated on historical data, so that I can trust the accuracy of demand predictions.

#### Acceptance Criteria

1. WHEN the training pipeline processes historical data THEN the Forecast Engine SHALL fill missing dates with zero units and aggregate usage by day
2. WHEN the model is trained THEN the Forecast Engine SHALL use the last 30 days of data as the test set and earlier data as the training set
3. WHEN model evaluation is performed THEN the Forecast Engine SHALL calculate Mean Absolute Error and Mean Absolute Percentage Error on the test set
4. WHEN forecast predictions are generated THEN the Forecast Engine SHALL use Prophet or ARIMA time-series models with 180 days of historical usage data
5. WHEN the forecast API is called THEN the Blood Bank System SHALL return JSON containing hospital identifier, blood group, component, forecast array with date and predicted values, and generation timestamp

### Requirement 11

**User Story:** As a system administrator, I want monitoring and logging capabilities, so that I can track system health, model performance, and troubleshoot issues.

#### Acceptance Criteria

1. WHEN an error occurs during CSV parsing THEN the Blood Bank System SHALL log the error with timestamp, file name, and error description
2. WHEN the daily forecast job runs THEN the Blood Bank System SHALL log the job start time, completion time, and number of forecasts generated
3. WHEN the system detects model drift THEN the Blood Bank System SHALL compare weekly forecast accuracy against actual usage and log the deviation
4. WHEN the admin dashboard loads THEN the Blood Bank System SHALL display a model drift metric showing forecast versus actual comparison for the past week
5. WHEN API requests fail THEN the Blood Bank System SHALL log the request details, error code, and error message for debugging

### Requirement 12

**User Story:** As a developer, I want clear deployment instructions and a containerized application, so that I can deploy the system to cloud platforms with minimal configuration.

#### Acceptance Criteria

1. WHEN the application is packaged THEN the Blood Bank System SHALL include a Dockerfile with backend, gunicorn server, and PostgreSQL database configuration
2. WHEN the deployment documentation is provided THEN the Blood Bank System SHALL include step-by-step instructions for local development setup
3. WHEN the deployment documentation is provided THEN the Blood Bank System SHALL include one-click deployment instructions for Heroku, Render, or Streamlit Cloud
4. WHERE external SMS gateway is used, WHEN the application starts THEN the Blood Bank System SHALL load API keys from environment variables or secrets management
5. WHEN seed data is provided THEN the Blood Bank System SHALL include CSV files for 3 hospitals within 30 kilometers with 6 months of daily usage per blood group
