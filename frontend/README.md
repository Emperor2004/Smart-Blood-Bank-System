# Smart Blood Bank - Frontend

This is a minimal React + Vite frontend for the Smart Blood Bank System. It provides two simple flows:

- Inventory CSV upload (POST /api/inventory/upload)
- Forecast viewer (GET /api/forecast)

Quick start

```bash
cd frontend
npm install
npm run dev
```

By default the frontend expects the backend at `http://localhost:8000`. You can change that by creating a `.env` file with:

```
VITE_BACKEND_URL=http://localhost:8000
```

Docker (optional)

Build and run a production image:

```bash
docker build -t smart-blood-bank-frontend .
docker run -p 3000:3000 smart-blood-bank-frontend
```
