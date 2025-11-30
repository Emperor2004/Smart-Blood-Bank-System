# 🔧 Configuration Guide - What to Change

## **File to Edit: `.env`**

Location: `/home/emperor/Projects/Smart Blood Bank System/.env`

---

## **1. SMS Notifications (Twilio)**

### **Where to Get Credentials:**
1. Go to https://www.twilio.com/
2. Sign up for free account (gets $15 credit)
3. Get your credentials from Console Dashboard

### **What to Change in `.env`:**
```bash
# Change these lines:
SMS_GATEWAY_ENABLED=True                          # Change False to True
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxx     # Your Account SID
TWILIO_AUTH_TOKEN=your_auth_token_here           # Your Auth Token
TWILIO_PHONE_NUMBER=+1234567890                  # Your Twilio phone number
```

### **Example:**
```bash
SMS_GATEWAY_ENABLED=True
TWILIO_ACCOUNT_SID=AC1234567890abcdef1234567890abcd
TWILIO_AUTH_TOKEN=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
TWILIO_PHONE_NUMBER=+15551234567
```

---

## **2. Email Notifications (Gmail)**

### **Where to Get Credentials:**
1. Use your Gmail account
2. Enable 2-Factor Authentication
3. Generate App Password: https://myaccount.google.com/apppasswords

### **What to Change in `.env`:**
```bash
# Change these lines:
EMAIL_ENABLED=True                               # Change False to True
SMTP_HOST=smtp.gmail.com                         # Keep as is for Gmail
SMTP_PORT=587                                    # Keep as is
SMTP_USER=your_email@gmail.com                   # Your Gmail address
SMTP_PASSWORD=your_16_char_app_password          # Your App Password
EMAIL_FROM=noreply@bloodbank.gov.in              # Sender name (can customize)
```

### **Example:**
```bash
EMAIL_ENABLED=True
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=myemail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
EMAIL_FROM=bloodbank@hospital.com
```

---

## **3. e-RaktKosh API Integration**

### **Where to Get Credentials:**
1. Contact e-RaktKosh team: https://www.eraktkosh.in/
2. Request API access for your hospital
3. Get API key from their portal

### **What to Change in `.env`:**
```bash
# Change these lines:
ERAKTKOSH_API_ENABLED=True                       # Change False to True
ERAKTKOSH_API_URL=https://api.eraktkosh.in       # Keep as is (or use provided URL)
ERAKTKOSH_API_KEY=your_api_key_here              # Your API key
```

### **Example:**
```bash
ERAKTKOSH_API_ENABLED=True
ERAKTKOSH_API_URL=https://api.eraktkosh.in
ERAKTKOSH_API_KEY=erk_live_1234567890abcdef
```

---

## **4. Security Keys (IMPORTANT - Change in Production)**

### **What to Change in `.env`:**
```bash
# Generate random 32+ character strings:
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
ENCRYPTION_KEY=your-encryption-key-for-sensitive-data-32-bytes
```

### **How to Generate Secure Keys:**
```bash
# Run this in terminal to generate random keys:
openssl rand -hex 32
```

### **Example:**
```bash
SECRET_KEY=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
JWT_SECRET_KEY=z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4j3i2h1g0f9e8d7c6b5a4
ENCRYPTION_KEY=1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
```

---

## **5. Database (Optional - Only if Changing Defaults)**

### **What to Change in `.env`:**
```bash
# Only change if you want different credentials:
DB_USER=bloodbank                                # Database username
DB_PASSWORD=bloodbank123                         # Database password
DB_NAME=smart_blood_bank                         # Database name
DB_HOST=localhost                                # Keep as localhost for Docker
DB_PORT=5432                                     # Keep as 5432
```

---

## **6. Frontend API URL (If Backend on Different Server)**

### **File to Edit:** `frontend/.env`

```bash
# Change this if backend is on different server:
VITE_API_URL=http://localhost:8000              # Your backend URL
```

### **Example for Production:**
```bash
VITE_API_URL=https://api.yourserver.com
```

---

## **Quick Setup Commands**

### **1. Copy and Edit .env File:**
```bash
cd "/home/emperor/Projects/Smart Blood Bank System"
nano .env
# Edit the values above
# Press Ctrl+X, then Y, then Enter to save
```

### **2. Restart Services:**
```bash
docker-compose down
docker-compose up -d
```

---

## **Testing Configuration**

### **Test SMS (After Adding Twilio Credentials):**
```bash
curl -X POST "http://localhost:8000/api/notifications/donor" \
  -H "Content-Type: application/json" \
  -d '{
    "donor_id": 1,
    "donor_phone": "+1234567890",
    "hospital_name": "Test Hospital",
    "blood_group": "O+",
    "contact_phone": "+0987654321"
  }'
```

### **Test e-RaktKosh (After Adding API Key):**
```bash
curl "http://localhost:8000/api/eraktkosh/status"
```

---

## **Summary - What You MUST Change:**

### **For Basic Operation (No Changes Needed):**
- ✅ System works out of the box
- ✅ SMS/Email in simulation mode (prints to console)

### **For SMS Notifications:**
- 📝 Add Twilio credentials (4 lines in `.env`)

### **For Email Notifications:**
- 📝 Add Gmail credentials (2 lines in `.env`)

### **For e-RaktKosh:**
- 📝 Add API key (1 line in `.env`)

### **For Production Security:**
- 📝 Change SECRET_KEY, JWT_SECRET_KEY, ENCRYPTION_KEY (3 lines in `.env`)

---

## **Need Help?**

### **Get Twilio Free Account:**
https://www.twilio.com/try-twilio

### **Generate Gmail App Password:**
https://support.google.com/accounts/answer/185833

### **Generate Secure Keys:**
```bash
openssl rand -hex 32
```

---

**That's it! Just edit `.env` file with your credentials.**
