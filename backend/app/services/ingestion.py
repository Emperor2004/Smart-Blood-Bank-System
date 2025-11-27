"""Data ingestion service for CSV validation and parsing."""
import pandas as pd
from typing import List, Dict, Tuple, Optional
from datetime import datetime
from io import StringIO
from app.schemas.inventory import InventoryCreate
from app.schemas.enums import BloodGroup, Component


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class IngestionResult:
    """Result of CSV ingestion operation."""
    def __init__(self):
        self.valid_records: List[InventoryCreate] = []
        self.errors: List[Dict[str, str]] = []
        self.duplicates: List[str] = []
        self.success_count: int = 0
        self.error_count: int = 0
        
    def add_valid_record(self, record: InventoryCreate):
        """Add a valid record."""
        self.valid_records.append(record)
        self.success_count += 1
        
    def add_error(self, row_num: int, field: str, message: str, value: Optional[str] = None):
        """Add an error."""
        error = {
            "row": row_num,
            "field": field,
            "message": message
        }
        if value is not None:
            error["value"] = value
        self.errors.append(error)
        self.error_count += 1
        
    def add_duplicate(self, record_id: str):
        """Add a duplicate record ID."""
        self.duplicates.append(record_id)
        self.error_count += 1


class IngestionService:
    """Service for CSV validation and parsing."""
    
    # Blood group normalization mappings
    BLOOD_GROUP_MAPPINGS = {
        # Standard forms
        "A+": "A+", "A-": "A-",
        "B+": "B+", "B-": "B-",
        "AB+": "AB+", "AB-": "AB-",
        "O+": "O+", "O-": "O-",
        # Lowercase
        "a+": "A+", "a-": "A-",
        "b+": "B+", "b-": "B-",
        "ab+": "AB+", "ab-": "AB-",
        "o+": "O+", "o-": "O-",
        # With spaces
        "A +": "A+", "A -": "A-",
        "B +": "B+", "B -": "B-",
        "AB +": "AB+", "AB -": "AB-",
        "O +": "O+", "O -": "O-",
        # Full names
        "A POSITIVE": "A+", "A NEGATIVE": "A-",
        "B POSITIVE": "B+", "B NEGATIVE": "B-",
        "AB POSITIVE": "AB+", "AB NEGATIVE": "AB-",
        "O POSITIVE": "O+", "O NEGATIVE": "O-",
        # Title case
        "A Positive": "A+", "A Negative": "A-",
        "B Positive": "B+", "B Negative": "B-",
        "AB Positive": "AB+", "AB Negative": "AB-",
        "O Positive": "O+", "O Negative": "O-",
        # Lowercase full names
        "a positive": "A+", "a negative": "A-",
        "b positive": "B+", "b negative": "B-",
        "ab positive": "AB+", "ab negative": "AB-",
        "o positive": "O+", "o negative": "O-",
    }
    
    REQUIRED_COLUMNS = [
        'record_id',
        'hospital_id',
        'blood_group',
        'component',
        'units',
        'unit_expiry_date',
        'collection_date'
    ]
    
    def normalize_blood_group(self, blood_group: str) -> str:
        """
        Normalize blood group value to standard format.
        
        Args:
            blood_group: Blood group string to normalize
            
        Returns:
            Normalized blood group (e.g., "A+", "O-")
            
        Raises:
            ValueError: If blood group is not recognized
        """
        if not blood_group or not isinstance(blood_group, str):
            raise ValueError(f"Invalid blood group: {blood_group}")
        
        # Strip whitespace and convert to uppercase for lookup
        normalized_key = blood_group.strip().upper()
        
        # Try direct lookup first
        if normalized_key in self.BLOOD_GROUP_MAPPINGS:
            return self.BLOOD_GROUP_MAPPINGS[normalized_key]
        
        # Try with original casing
        if blood_group.strip() in self.BLOOD_GROUP_MAPPINGS:
            return self.BLOOD_GROUP_MAPPINGS[blood_group.strip()]
        
        raise ValueError(f"Unrecognized blood group: {blood_group}")
    
    def validate_csv_format(self, file_content: str) -> Tuple[bool, Optional[str]]:
        """
        Validate CSV file format.
        
        Args:
            file_content: CSV file content as string
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            df = pd.read_csv(StringIO(file_content))
        except Exception as e:
            return False, f"Failed to parse CSV: {str(e)}"
        
        # Check for required columns
        missing_columns = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing_columns:
            return False, f"Missing required columns: {', '.join(missing_columns)}"
        
        # Check if file is empty
        if len(df) == 0:
            return False, "CSV file is empty"
        
        return True, None
    
    def check_duplicates(self, record_ids: List[str]) -> List[str]:
        """
        Check for duplicate record IDs.
        
        Args:
            record_ids: List of record IDs to check
            
        Returns:
            List of duplicate record IDs
        """
        seen = set()
        duplicates = []
        
        for record_id in record_ids:
            if record_id in seen:
                if record_id not in duplicates:
                    duplicates.append(record_id)
            else:
                seen.add(record_id)
        
        return duplicates
    
    def parse_csv(self, file_content: str) -> IngestionResult:
        """
        Parse and validate CSV file content.
        
        Args:
            file_content: CSV file content as string
            
        Returns:
            IngestionResult with valid records and errors
        """
        result = IngestionResult()
        
        # Validate format first
        is_valid, error_msg = self.validate_csv_format(file_content)
        if not is_valid:
            result.add_error(0, "file", error_msg)
            return result
        
        # Parse CSV
        df = pd.read_csv(StringIO(file_content))
        
        # Check for duplicates
        duplicates = self.check_duplicates(df['record_id'].tolist())
        for dup_id in duplicates:
            result.add_duplicate(dup_id)
        
        # Process each row
        for idx, row in df.iterrows():
            row_num = idx + 2  # +2 because: 0-indexed + header row
            
            try:
                # Skip if this is a duplicate
                if row['record_id'] in duplicates:
                    result.add_error(row_num, "record_id", f"Duplicate record ID: {row['record_id']}")
                    continue
                
                # Validate and normalize blood group
                try:
                    normalized_blood_group = self.normalize_blood_group(str(row['blood_group']))
                except ValueError as e:
                    result.add_error(row_num, "blood_group", str(e), str(row['blood_group']))
                    continue
                
                # Validate component
                component_str = str(row['component']).strip()
                if component_str not in [c.value for c in Component]:
                    result.add_error(
                        row_num, 
                        "component", 
                        f"Invalid component. Must be one of: {', '.join([c.value for c in Component])}",
                        component_str
                    )
                    continue
                
                # Validate units
                try:
                    units = int(row['units'])
                    if units <= 0:
                        result.add_error(row_num, "units", "Units must be greater than 0", str(units))
                        continue
                except (ValueError, TypeError):
                    result.add_error(row_num, "units", "Units must be a positive integer", str(row['units']))
                    continue
                
                # Parse dates
                try:
                    collection_date = pd.to_datetime(row['collection_date']).date()
                except Exception as e:
                    result.add_error(row_num, "collection_date", f"Invalid date format: {str(e)}", str(row['collection_date']))
                    continue
                
                try:
                    unit_expiry_date = pd.to_datetime(row['unit_expiry_date']).date()
                except Exception as e:
                    result.add_error(row_num, "unit_expiry_date", f"Invalid date format: {str(e)}", str(row['unit_expiry_date']))
                    continue
                
                # Validate expiry date is after collection date
                if unit_expiry_date < collection_date:
                    result.add_error(
                        row_num,
                        "unit_expiry_date",
                        "Expiry date must be after collection date"
                    )
                    continue
                
                # Create valid record
                record = InventoryCreate(
                    record_id=str(row['record_id']).strip(),
                    hospital_id=str(row['hospital_id']).strip(),
                    blood_group=BloodGroup(normalized_blood_group),
                    component=Component(component_str),
                    units=units,
                    unit_expiry_date=unit_expiry_date,
                    collection_date=collection_date
                )
                
                result.add_valid_record(record)
                
            except Exception as e:
                result.add_error(row_num, "general", f"Unexpected error: {str(e)}")
        
        return result
