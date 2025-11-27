"""Donor repository for database operations."""
from typing import List, Optional
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.donor import Donor
from app.schemas.donor import DonorCreate
from app.utils.encryption import encrypt_value, decrypt_value
from app.config import settings


class DonorRepository:
    """Repository for donor CRUD operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
        self.eligibility_days = settings.donor_eligibility_days
    
    def create(self, donor: DonorCreate) -> Donor:
        """
        Create a new donor record with encrypted contact info.
        
        Args:
            donor: Donor data to create
            
        Returns:
            Created donor record
        """
        # Encrypt sensitive fields
        encrypted_phone = encrypt_value(donor.phone) if donor.phone else None
        encrypted_email = encrypt_value(donor.email) if donor.email else None
        
        # Calculate eligibility
        eligible = self._calculate_eligibility(donor.last_donation_date)
        
        db_donor = Donor(
            name=donor.name,
            phone=encrypted_phone,
            email=encrypted_email,
            blood_group=donor.blood_group.value,
            last_donation_date=donor.last_donation_date,
            eligible=eligible,
            location_lat=donor.location_lat,
            location_lon=donor.location_lon
        )
        self.db.add(db_donor)
        self.db.commit()
        self.db.refresh(db_donor)
        return db_donor
    
    def get_by_id(self, donor_id: int) -> Optional[Donor]:
        """Get donor record by ID."""
        return self.db.query(Donor).filter(Donor.donor_id == donor_id).first()
    
    def get_all(self) -> List[Donor]:
        """Get all donor records."""
        return self.db.query(Donor).all()
    
    def search_donors(
        self,
        blood_group: Optional[str] = None,
        eligible_only: bool = False,
        hospital_lat: Optional[float] = None,
        hospital_lon: Optional[float] = None,
        radius_km: Optional[float] = None
    ) -> List[Donor]:
        """
        Search for donors with filters.
        
        Args:
            blood_group: Optional blood group filter
            eligible_only: Filter for eligible donors only
            hospital_lat: Hospital latitude for radius search
            hospital_lon: Hospital longitude for radius search
            radius_km: Search radius in kilometers
            
        Returns:
            List of matching donor records
        """
        query = self.db.query(Donor)
        
        if blood_group:
            query = query.filter(Donor.blood_group == blood_group)
        
        if eligible_only:
            query = query.filter(Donor.eligible == True)
        
        # Note: For radius filtering, we'd need PostGIS or calculate in Python
        # For now, get all matching donors and filter by distance in service layer
        
        return query.all()
    
    def update_eligibility(self, donor_id: int) -> Optional[Donor]:
        """
        Update donor eligibility based on last donation date.
        
        Args:
            donor_id: Donor ID to update
            
        Returns:
            Updated donor record or None if not found
        """
        donor = self.get_by_id(donor_id)
        if not donor:
            return None
        
        donor.eligible = self._calculate_eligibility(donor.last_donation_date)
        self.db.commit()
        self.db.refresh(donor)
        return donor
    
    def update_all_eligibility(self) -> int:
        """
        Update eligibility for all donors.
        
        Returns:
            Number of donors updated
        """
        donors = self.get_all()
        count = 0
        
        for donor in donors:
            new_eligible = self._calculate_eligibility(donor.last_donation_date)
            if donor.eligible != new_eligible:
                donor.eligible = new_eligible
                count += 1
        
        self.db.commit()
        return count
    
    def _calculate_eligibility(self, last_donation_date: Optional[date]) -> bool:
        """
        Calculate if donor is eligible based on last donation date.
        
        Args:
            last_donation_date: Last donation date
            
        Returns:
            True if eligible, False otherwise
        """
        if not last_donation_date:
            return True
        
        days_since_donation = (date.today() - last_donation_date).days
        return days_since_donation > self.eligibility_days
    
    def decrypt_contact_info(self, donor: Donor) -> dict:
        """
        Decrypt donor contact information.
        
        Args:
            donor: Donor record
            
        Returns:
            Dictionary with decrypted contact info
        """
        return {
            "donor_id": donor.donor_id,
            "name": donor.name,
            "phone": decrypt_value(donor.phone) if donor.phone else None,
            "email": decrypt_value(donor.email) if donor.email else None,
            "blood_group": donor.blood_group,
            "last_donation_date": donor.last_donation_date,
            "eligible": donor.eligible,
            "location_lat": float(donor.location_lat) if donor.location_lat else None,
            "location_lon": float(donor.location_lon) if donor.location_lon else None
        }
