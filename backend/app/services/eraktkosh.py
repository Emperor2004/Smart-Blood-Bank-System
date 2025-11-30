"""e-RaktKosh API integration service."""
from typing import List, Dict, Optional
import httpx
from datetime import date
from app.config import settings


class ERaktKoshService:
    """Service for e-RaktKosh API integration."""
    
    def __init__(self):
        """Initialize service."""
        self.enabled = settings.eraktkosh_api_enabled
        self.api_url = settings.eraktkosh_api_url
        self.api_key = settings.eraktkosh_api_key
        self.timeout = 30.0
    
    def _get_headers(self) -> Dict[str, str]:
        """Get API request headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def fetch_inventory(self, hospital_id: str) -> Optional[List[Dict]]:
        """
        Fetch inventory data from e-RaktKosh.
        
        Args:
            hospital_id: Hospital ID in e-RaktKosh system
            
        Returns:
            List of inventory records or None if error
        """
        if not self.enabled:
            print("[e-RaktKosh] Integration disabled")
            return None
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.api_url}/inventory/{hospital_id}",
                    headers=self._get_headers()
                )
                response.raise_for_status()
                data = response.json()
                return self._transform_inventory(data)
        except Exception as e:
            print(f"[e-RaktKosh ERROR] {str(e)}")
            return None
    
    def _transform_inventory(self, data: Dict) -> List[Dict]:
        """Transform e-RaktKosh format to internal format."""
        records = []
        for item in data.get("inventory", []):
            records.append({
                "record_id": item.get("id"),
                "hospital_id": item.get("hospital_id"),
                "blood_group": item.get("blood_group"),
                "component": item.get("component_type"),
                "units": item.get("quantity"),
                "unit_expiry_date": item.get("expiry_date"),
                "collection_date": item.get("collection_date")
            })
        return records
    
    async def sync_inventory(self, hospital_id: str) -> Dict:
        """
        Sync inventory from e-RaktKosh.
        
        Args:
            hospital_id: Hospital ID
            
        Returns:
            Sync result with count
        """
        records = await self.fetch_inventory(hospital_id)
        
        if records is None:
            return {"success": False, "error": "Failed to fetch from e-RaktKosh"}
        
        return {
            "success": True,
            "count": len(records),
            "records": records
        }
