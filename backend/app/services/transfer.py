"""Transfer recommendation service."""
from typing import List, Dict, Optional, Tuple
from datetime import date, timedelta
from math import radians, cos, sin, asin, sqrt
from sqlalchemy.orm import Session
from app.repositories.hospital import HospitalRepository
from app.repositories.inventory import InventoryRepository
from app.repositories.forecast import ForecastRepository
from app.repositories.transfer import TransferRepository
from app.config import settings


class TransferService:
    """Service for transfer recommendations."""
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.hospital_repo = HospitalRepository(db)
        self.inventory_repo = InventoryRepository(db)
        self.forecast_repo = ForecastRepository(db)
        self.transfer_repo = TransferRepository(db)
        self.radius_km = settings.transfer_radius_km
        self.surplus_threshold = settings.transfer_surplus_threshold
        self.weight_expiry = settings.transfer_weight_expiry
        self.weight_distance = settings.transfer_weight_distance
        self.weight_surplus = settings.transfer_weight_surplus
        self.speed_kmh = settings.transfer_speed_kmh
    
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
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        
        # Earth radius in kilometers
        r = 6371
        
        return c * r
    
    def find_nearby_hospitals(
        self,
        hospital_id: str,
        radius_km: Optional[float] = None
    ) -> List[Dict]:
        """
        Find hospitals within radius.
        
        Args:
            hospital_id: Source hospital ID
            radius_km: Search radius (uses config default if not provided)
            
        Returns:
            List of nearby hospitals with distances
        """
        if radius_km is None:
            radius_km = self.radius_km
        
        source_hospital = self.hospital_repo.get_by_id(hospital_id)
        if not source_hospital or not source_hospital.latitude or not source_hospital.longitude:
            return []
        
        all_hospitals = self.hospital_repo.get_all()
        nearby = []
        
        for hospital in all_hospitals:
            if hospital.hospital_id == hospital_id:
                continue
            
            if not hospital.latitude or not hospital.longitude:
                continue
            
            distance = self.haversine_distance(
                source_hospital.latitude,
                source_hospital.longitude,
                hospital.latitude,
                hospital.longitude
            )
            
            if distance <= radius_km:
                nearby.append({
                    "hospital_id": hospital.hospital_id,
                    "name": hospital.name,
                    "distance_km": round(distance, 2),
                    "latitude": float(hospital.latitude),
                    "longitude": float(hospital.longitude)
                })
        
        return sorted(nearby, key=lambda x: x["distance_km"])
    
    def calculate_deficit_and_surplus(
        self,
        hospital_id: str,
        forecast_days: int = 7
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Calculate deficit and surplus for hospital.
        
        Args:
            hospital_id: Hospital ID
            forecast_days: Days to forecast
            
        Returns:
            Tuple of (deficits, surpluses)
        """
        # Get inventory
        inventory = self.inventory_repo.get_all(
            filters={"hospital_id": hospital_id}
        )
        
        # Get forecasts
        forecasts = self.forecast_repo.get_latest_forecasts(
            hospital_id=hospital_id,
            days=forecast_days
        )
        
        # Aggregate by blood_group and component
        inventory_totals = {}
        for inv in inventory:
            key = f"{inv.blood_group}_{inv.component}"
            inventory_totals[key] = inventory_totals.get(key, 0) + inv.units
        
        forecast_totals = {}
        for fc in forecasts:
            key = f"{fc.blood_group}_{fc.component}"
            forecast_totals[key] = forecast_totals.get(key, 0) + float(fc.predicted_units)
        
        # Calculate deficits and surpluses
        deficits = []
        surpluses = []
        
        all_keys = set(inventory_totals.keys()) | set(forecast_totals.keys())
        
        for key in all_keys:
            blood_group, component = key.split("_")
            inv_total = inventory_totals.get(key, 0)
            fc_total = forecast_totals.get(key, 0)
            
            diff = inv_total - fc_total
            
            if diff < 0:  # Deficit
                deficits.append({
                    "blood_group": blood_group,
                    "component": component,
                    "deficit": abs(diff)
                })
            elif diff > self.surplus_threshold:  # Surplus
                surpluses.append({
                    "blood_group": blood_group,
                    "component": component,
                    "surplus": diff
                })
        
        return deficits, surpluses
    
    def calculate_urgency_score(
        self,
        days_to_expiry: int,
        distance_km: float,
        surplus: float,
        max_days: int = 30,
        max_distance: float = 100,
        max_surplus: float = 100
    ) -> float:
        """
        Calculate transfer urgency score.
        
        Args:
            days_to_expiry: Days until expiry
            distance_km: Distance in km
            surplus: Surplus units
            max_days: Maximum days for normalization
            max_distance: Maximum distance for normalization
            max_surplus: Maximum surplus for normalization
            
        Returns:
            Urgency score (0-1)
        """
        # Normalize values
        norm_expiry = min(days_to_expiry / max_days, 1.0)
        norm_distance = min(distance_km / max_distance, 1.0)
        norm_surplus = min(surplus / max_surplus, 1.0)
        
        # Calculate weighted score
        score = (
            self.weight_expiry * (1 - norm_expiry) +
            self.weight_distance * (1 - norm_distance) +
            self.weight_surplus * norm_surplus
        )
        
        return score
    
    def calculate_eta(self, distance_km: float) -> int:
        """
        Calculate estimated time of arrival in minutes.
        
        Args:
            distance_km: Distance in kilometers
            
        Returns:
            ETA in minutes
        """
        hours = distance_km / self.speed_kmh
        minutes = hours * 60
        return round(minutes)
    
    def generate_recommendations(
        self,
        hospital_id: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate transfer recommendations.
        
        Args:
            hospital_id: Optional hospital ID filter
            
        Returns:
            List of transfer recommendations sorted by urgency
        """
        recommendations = []
        
        # Get hospitals to process
        if hospital_id:
            hospitals = [self.hospital_repo.get_by_id(hospital_id)]
        else:
            hospitals = self.hospital_repo.get_all()
        
        for hospital in hospitals:
            if not hospital:
                continue
            
            # Get deficits for this hospital
            deficits, _ = self.calculate_deficit_and_surplus(hospital.hospital_id)
            
            if not deficits:
                continue
            
            # Find nearby hospitals
            nearby = self.find_nearby_hospitals(hospital.hospital_id)
            
            for deficit in deficits:
                # Find hospitals with surplus of this blood type
                for nearby_hospital in nearby:
                    _, surpluses = self.calculate_deficit_and_surplus(
                        nearby_hospital["hospital_id"]
                    )
                    
                    for surplus in surpluses:
                        if (surplus["blood_group"] == deficit["blood_group"] and
                            surplus["component"] == deficit["component"]):
                            
                            # Get inventory with earliest expiry
                            source_inv = self.inventory_repo.get_all(
                                filters={
                                    "hospital_id": nearby_hospital["hospital_id"],
                                    "blood_group": deficit["blood_group"],
                                    "component": deficit["component"]
                                }
                            )
                            
                            if not source_inv:
                                continue
                            
                            # Sort by expiry date
                            source_inv.sort(key=lambda x: x.unit_expiry_date)
                            earliest = source_inv[0]
                            
                            days_to_expiry = (earliest.unit_expiry_date - date.today()).days
                            
                            # Calculate urgency score
                            urgency = self.calculate_urgency_score(
                                days_to_expiry=days_to_expiry,
                                distance_km=nearby_hospital["distance_km"],
                                surplus=surplus["surplus"]
                            )
                            
                            # Calculate ETA
                            eta = self.calculate_eta(nearby_hospital["distance_km"])
                            
                            # Determine units to transfer
                            units = min(deficit["deficit"], surplus["surplus"], earliest.units)
                            
                            recommendations.append({
                                "source_hospital_id": nearby_hospital["hospital_id"],
                                "source_hospital_name": nearby_hospital["name"],
                                "destination_hospital_id": hospital.hospital_id,
                                "destination_hospital_name": hospital.name,
                                "blood_group": deficit["blood_group"],
                                "component": deficit["component"],
                                "units": int(units),
                                "urgency_score": round(urgency, 3),
                                "distance_km": nearby_hospital["distance_km"],
                                "eta_minutes": eta,
                                "days_to_expiry": days_to_expiry
                            })
        
        # Sort by urgency score (descending)
        recommendations.sort(key=lambda x: x["urgency_score"], reverse=True)
        
        return recommendations
    
    def approve_transfer(
        self,
        source_hospital_id: str,
        destination_hospital_id: str,
        blood_group: str,
        component: str,
        units: int,
        approved_by: str
    ) -> Dict:
        """
        Approve and execute transfer.
        
        Args:
            source_hospital_id: Source hospital ID
            destination_hospital_id: Destination hospital ID
            blood_group: Blood group
            component: Component
            units: Number of units
            approved_by: User ID who approved
            
        Returns:
            Transfer record
        """
        # Get source inventory
        source_inv = self.inventory_repo.get_all(
            filters={
                "hospital_id": source_hospital_id,
                "blood_group": blood_group,
                "component": component
            }
        )
        
        if not source_inv:
            raise ValueError("No source inventory found")
        
        # Sort by expiry date (use oldest first)
        source_inv.sort(key=lambda x: x.unit_expiry_date)
        
        # Update inventories
        remaining_units = units
        for inv in source_inv:
            if remaining_units <= 0:
                break
            
            if inv.units <= remaining_units:
                # Delete this record
                self.inventory_repo.delete(inv.record_id)
                remaining_units -= inv.units
            else:
                # Update this record
                self.inventory_repo.update(
                    inv.record_id,
                    {"units": inv.units - remaining_units}
                )
                remaining_units = 0
        
        # Create transfer record
        transfer = self.transfer_repo.create({
            "source_hospital_id": source_hospital_id,
            "destination_hospital_id": destination_hospital_id,
            "blood_group": blood_group,
            "component": component,
            "units": units,
            "status": "approved",
            "approved_by": approved_by
        })
        
        return transfer
