"""Seed data script for demo and testing."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, timedelta
import random
from app.database import SessionLocal
from app.repositories.hospital import HospitalRepository
from app.repositories.inventory import InventoryRepository
from app.repositories.usage import UsageRepository
from app.repositories.donor import DonorRepository
from app.repositories.user import UserRepository
from app.schemas.hospital import HospitalCreate
from app.schemas.inventory import InventoryCreate
from app.schemas.usage import UsageCreate
from app.schemas.donor import DonorCreate
from app.schemas.enums import BloodGroup, Component, Purpose


def seed_hospitals(db):
    """Seed hospital data."""
    print("Seeding hospitals...")
    hospital_repo = HospitalRepository(db)
    
    hospitals = [
        {
            "hospital_id": "H001",
            "name": "Mumbai Central Hospital",
            "address": "Mumbai Central, Mumbai, Maharashtra",
            "latitude": 19.0760,
            "longitude": 72.8777,
            "contact_name": "Dr. Sharma",
            "contact_phone": "+91-22-12345678",
            "contact_email": "contact@mumbaicentral.gov.in"
        },
        {
            "hospital_id": "H002",
            "name": "Thane General Hospital",
            "address": "Thane West, Thane, Maharashtra",
            "latitude": 19.2183,
            "longitude": 72.9781,
            "contact_name": "Dr. Patel",
            "contact_phone": "+91-22-23456789",
            "contact_email": "contact@thanehospital.gov.in"
        },
        {
            "hospital_id": "H003",
            "name": "Navi Mumbai Medical Center",
            "address": "Vashi, Navi Mumbai, Maharashtra",
            "latitude": 19.0330,
            "longitude": 73.0297,
            "contact_name": "Dr. Kumar",
            "contact_phone": "+91-22-34567890",
            "contact_email": "contact@navimumbai.gov.in"
        }
    ]
    
    for h in hospitals:
        try:
            hospital_repo.create(HospitalCreate(**h))
            print(f"  Created hospital: {h['name']}")
        except:
            print(f"  Hospital {h['name']} already exists")


def seed_inventory(db):
    """Seed inventory data."""
    print("Seeding inventory...")
    inventory_repo = InventoryRepository(db)
    
    hospitals = ["H001", "H002", "H003"]
    blood_groups = list(BloodGroup)
    components = list(Component)
    
    record_count = 0
    for hospital_id in hospitals:
        for blood_group in blood_groups:
            for component in components:
                # Create 2-3 records per combination
                for i in range(random.randint(2, 3)):
                    record_id = f"{hospital_id}_{blood_group.value}_{component.value}_{i+1}"
                    units = random.randint(5, 50)
                    collection_date = date.today() - timedelta(days=random.randint(1, 30))
                    expiry_days = random.randint(5, 60)
                    expiry_date = collection_date + timedelta(days=expiry_days)
                    
                    try:
                        inventory_repo.create(InventoryCreate(
                            record_id=record_id,
                            hospital_id=hospital_id,
                            blood_group=blood_group,
                            component=component,
                            units=units,
                            unit_expiry_date=expiry_date,
                            collection_date=collection_date
                        ))
                        record_count += 1
                    except:
                        pass
    
    print(f"  Created {record_count} inventory records")


def seed_usage(db):
    """Seed usage data (6 months)."""
    print("Seeding usage data...")
    usage_repo = UsageRepository(db)
    
    hospitals = ["H001", "H002", "H003"]
    blood_groups = list(BloodGroup)
    components = list(Component)
    purposes = list(Purpose)
    
    record_count = 0
    end_date = date.today()
    start_date = end_date - timedelta(days=180)
    
    current_date = start_date
    while current_date <= end_date:
        for hospital_id in hospitals:
            for blood_group in blood_groups:
                for component in components:
                    # Random usage (0-10 units per day)
                    if random.random() > 0.3:  # 70% chance of usage
                        units_used = random.randint(1, 10)
                        purpose = random.choice(purposes)
                        
                        try:
                            usage_repo.create(UsageCreate(
                                hospital_id=hospital_id,
                                blood_group=blood_group,
                                component=component,
                                units_used=units_used,
                                usage_date=current_date,
                                purpose=purpose
                            ))
                            record_count += 1
                        except:
                            pass
        
        current_date += timedelta(days=1)
    
    print(f"  Created {record_count} usage records")


def seed_donors(db):
    """Seed donor data."""
    print("Seeding donors...")
    donor_repo = DonorRepository(db)
    
    first_names = ["Raj", "Priya", "Amit", "Sneha", "Vikram", "Anjali", "Rahul", "Pooja", "Arjun", "Kavya"]
    last_names = ["Sharma", "Patel", "Kumar", "Singh", "Reddy", "Nair", "Gupta", "Desai", "Mehta", "Joshi"]
    blood_groups = list(BloodGroup)
    
    # Mumbai area coordinates
    base_lat = 19.0760
    base_lon = 72.8777
    
    record_count = 0
    for i in range(100):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        phone = f"+91-{random.randint(7000000000, 9999999999)}"
        email = f"donor{i+1}@example.com"
        blood_group = random.choice(blood_groups)
        
        # Random last donation date (or None)
        if random.random() > 0.3:
            last_donation_date = date.today() - timedelta(days=random.randint(0, 180))
        else:
            last_donation_date = None
        
        # Random location within ~30km
        lat = base_lat + random.uniform(-0.3, 0.3)
        lon = base_lon + random.uniform(-0.3, 0.3)
        
        try:
            donor_repo.create(DonorCreate(
                name=name,
                phone=phone,
                email=email,
                blood_group=blood_group,
                last_donation_date=last_donation_date,
                location_lat=lat,
                location_lon=lon
            ))
            record_count += 1
        except:
            pass
    
    print(f"  Created {record_count} donor records")


def seed_users(db):
    """Seed user accounts."""
    print("Seeding users...")
    user_repo = UserRepository(db)
    
    users = [
        {"username": "admin", "password": "admin123", "role": "admin", "hospital_id": None},
        {"username": "staff1", "password": "staff123", "role": "staff", "hospital_id": "H001"},
        {"username": "staff2", "password": "staff123", "role": "staff", "hospital_id": "H002"},
        {"username": "staff3", "password": "staff123", "role": "staff", "hospital_id": "H003"},
    ]
    
    for u in users:
        try:
            user_repo.create(**u)
            print(f"  Created user: {u['username']}")
        except:
            print(f"  User {u['username']} already exists")


def main():
    """Main seed function."""
    print("Starting database seeding...")
    print("=" * 50)
    
    db = SessionLocal()
    
    try:
        seed_hospitals(db)
        seed_inventory(db)
        seed_usage(db)
        seed_donors(db)
        seed_users(db)
        
        print("=" * 50)
        print("✅ Database seeding completed successfully!")
        print("\nTest Credentials:")
        print("  Admin: username=admin, password=admin123")
        print("  Staff: username=staff1, password=staff123")
        
    except Exception as e:
        print(f"❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
