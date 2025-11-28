# Quick Test Commands

## Test Backend Health
```bash
curl https://yolande-nondivisional-norah.ngrok-free.dev/health
```

## Test CSV Upload
```bash
curl -X POST https://yolande-nondivisional-norah.ngrok-free.dev/api/inventory/upload \
  -F "file=@test_inventory.csv"
```

## View API Documentation
```bash
# Open in browser:
https://yolande-nondivisional-norah.ngrok-free.dev/docs
```

## Check Database
```bash
cd backend
source .venv/bin/activate
python3 -c "
from app.database import SessionLocal
from app.models.inventory import Inventory
db = SessionLocal()
count = db.query(Inventory).count()
print(f'Total inventory records: {count}')
db.close()
"
```

## Test Frontend
```bash
# Open in browser:
https://frontend-m8rqh0kc0-om-narayan-pandits-projects.vercel.app
```

## Check Running Services
```bash
# Backend
curl http://localhost:8000/health

# ngrok
curl http://localhost:4040/api/tunnels

# PostgreSQL
docker ps | grep postgres
```
