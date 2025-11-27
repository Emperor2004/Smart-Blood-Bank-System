"""Donor service for business logic."""
from typing import List, Optional
from math import radians, cos, sin, asin, sqrt
from sqlalchemy.orm import Session
from app.repositories.donor import DonorRepository
from app.schemas.donor import DonorCreate


class DonorService:
    """Service for donor management."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.repository = DonorRepository(db)
    
    def haversine_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """
        Calculate haversine distance between two points.
        
        Args:
            lat1, lon1: First point coordinates
            lat2, lon2: Second point coordinates
            
        Returns:
            Distance in kilometers
        """
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        r = 6371  # Earth radius in kilometers
        return c * r
    
    def register_donor(self, donor: DonorCreate) -> dict:
        """
        Register a new donor.
        
        Args:
            donor: Donor data
            
        Returns:
            Created donor with decrypted contact info
        """
        db_donor = self.repository.create(donor)
        return self.repository.decrypt_contact_info(db_donor)
    
    def search_donors(
        self,
        blood_group: Optional[str] = None,
        eligible_only: bool = False,
        hospital_lat: Optional[float] = None,
        hospital_lon: Optional[float] = None,
        radius_km: Optional[float] = None
    ) -> List[dict]:
        """
        Search for donors with filters.
        
        Args:
            blood_group: Optional blood group filter
            eligible_only: Filter for eligible donors only
            hospital_lat: Hospital latitude for radius search
            hospital_lon: Hospital longitude for radius search
            radius_km: Search radius in kilometers
            
        Returns:
            List of matching donors with decrypted contact info
        """
        # Get donors from repository
        donors = self.repository.search_donors(
            blood_group=blood_group,
            eligible_only=eligible_only
        )
        
        # Apply radius filter if coordinates provided
        if hospital_lat is not None and hospital_lon is not None and radius_km is not None:
            filtered_donors = []
            for donor in donors:
                if donor.location_lat is not None and donor.location_lon is not None:
                    distance = self.haversine_distance(
                        hospital_lat,
                        hospital_lon,
                        float(donor.location_lat),
                        float(donor.location_lon)
                    )
                    if distance <= radius_km:
                        donor_dict = self.repository.decrypt_contact_info(donor)
                        donor_dict['distance_km'] = round(distance, 2)
                        filtered_donors.append(donor_dict)
            
            # Sort by distance
            filtered_donors.sort(key=lambda x: x['distance_km'])
            return filtered_donors
        else:
            # No radius filter, return all matching donors
            return [self.repository.decrypt_contact_info(d) for d in donors]
    
    def get_donor_by_id(self, donor_id: int) -> Optional[dict]:
        """
        Get donor by ID with decrypted contact info.
        
        Args:
            donor_id: Donor ID
            
        Returns:
            Donor data or None if not found
        """
        donor = self.repository.get_by_id(donor_id)
        if not donor:
            return None
        return self.repository.decrypt_contact_info(donor)
    
    def update_eligibility(self, donor_id: int) -> Optional[dict]:
        """
        Update donor eligibility.
        
        Args:
            donor_id: Donor ID
            
        Returns:
            Updated donor data or None if not found
        """
        donor = self.repository.update_eligibility(donor_id)
        if not donor:
            return None
        return self.repository.decrypt_contact_info(donor)
