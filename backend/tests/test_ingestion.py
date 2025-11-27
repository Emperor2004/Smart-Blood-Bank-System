"""Tests for CSV ingestion service."""
import pytest
from datetime import date, timedelta
from backend.app.services.ingestion import IngestionService, IngestionResult
from backend.app.schemas.enums import BloodGroup, Component


class TestBloodGroupNormalization:
    """Tests for blood group normalization."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = IngestionService()
    
    def test_normalize_standard_forms(self):
        """Test normalization of standard blood group forms."""
        assert self.service.normalize_blood_group("A+") == "A+"
        assert self.service.normalize_blood_group("A-") == "A-"
        assert self.service.normalize_blood_group("B+") == "B+"
        assert self.service.normalize_blood_group("B-") == "B-"
        assert self.service.normalize_blood_group("AB+") == "AB+"
        assert self.service.normalize_blood_group("AB-") == "AB-"
        assert self.service.normalize_blood_group("O+") == "O+"
        assert self.service.normalize_blood_group("O-") == "O-"
    
    def test_normalize_lowercase(self):
        """Test normalization of lowercase blood groups."""
        assert self.service.normalize_blood_group("a+") == "A+"
        assert self.service.normalize_blood_group("a-") == "A-"
        assert self.service.normalize_blood_group("b+") == "B+"
        assert self.service.normalize_blood_group("o-") == "O-"
    
    def test_normalize_with_spaces(self):
        """Test normalization of blood groups with spaces."""
        assert self.service.normalize_blood_group("A +") == "A+"
        assert self.service.normalize_blood_group("B -") == "B-"
        assert self.service.normalize_blood_group(" A+ ") == "A+"
    
    def test_normalize_full_names(self):
        """Test normalization of full blood group names."""
        assert self.service.normalize_blood_group("A POSITIVE") == "A+"
        assert self.service.normalize_blood_group("A NEGATIVE") == "A-"
        assert self.service.normalize_blood_group("B Positive") == "B+"
        assert self.service.normalize_blood_group("b negative") == "B-"
        assert self.service.normalize_blood_group("AB Positive") == "AB+"
        assert self.service.normalize_blood_group("O Negative") == "O-"
    
    def test_normalize_invalid_blood_group(self):
        """Test that invalid blood groups raise ValueError."""
        with pytest.raises(ValueError, match="Unrecognized blood group"):
            self.service.normalize_blood_group("XYZ")
        
        with pytest.raises(ValueError, match="Unrecognized blood group"):
            self.service.normalize_blood_group("C+")
        
        with pytest.raises(ValueError, match="Invalid blood group"):
            self.service.normalize_blood_group("")
        
        with pytest.raises(ValueError, match="Invalid blood group"):
            self.service.normalize_blood_group(None)


class TestCSVValidation:
    """Tests for CSV format validation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = IngestionService()
    
    def test_validate_valid_csv(self):
        """Test validation of valid CSV format."""
        csv_content = """record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,2024-12-31,2024-11-01"""
        
        is_valid, error = self.service.validate_csv_format(csv_content)
        assert is_valid is True
        assert error is None
    
    def test_validate_missing_columns(self):
        """Test validation fails with missing columns."""
        csv_content = """record_id,hospital_id,blood_group
R001,H001,A+"""
        
        is_valid, error = self.service.validate_csv_format(csv_content)
        assert is_valid is False
        assert "Missing required columns" in error
    
    def test_validate_empty_csv(self):
        """Test validation fails with empty CSV."""
        csv_content = """record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date"""
        
        is_valid, error = self.service.validate_csv_format(csv_content)
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_validate_malformed_csv(self):
        """Test validation fails with malformed CSV."""
        csv_content = "not a valid csv format"
        
        is_valid, error = self.service.validate_csv_format(csv_content)
        assert is_valid is False
        assert "Missing required columns" in error


class TestDuplicateDetection:
    """Tests for duplicate record detection."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = IngestionService()
    
    def test_no_duplicates(self):
        """Test detection with no duplicates."""
        record_ids = ["R001", "R002", "R003"]
        duplicates = self.service.check_duplicates(record_ids)
        assert len(duplicates) == 0
    
    def test_single_duplicate(self):
        """Test detection of single duplicate."""
        record_ids = ["R001", "R002", "R001"]
        duplicates = self.service.check_duplicates(record_ids)
        assert len(duplicates) == 1
        assert "R001" in duplicates
    
    def test_multiple_duplicates(self):
        """Test detection of multiple duplicates."""
        record_ids = ["R001", "R002", "R001", "R003", "R002"]
        duplicates = self.service.check_duplicates(record_ids)
        assert len(duplicates) == 2
        assert "R001" in duplicates
        assert "R002" in duplicates
    
    def test_triple_duplicate(self):
        """Test detection when same ID appears three times."""
        record_ids = ["R001", "R001", "R001"]
        duplicates = self.service.check_duplicates(record_ids)
        assert len(duplicates) == 1
        assert "R001" in duplicates


class TestCSVParsing:
    """Tests for CSV parsing."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.service = IngestionService()
    
    def test_parse_valid_csv(self):
        """Test parsing of valid CSV."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,{future_date},{today}
R002,H001,B-,Platelets,3,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 2
        assert result.error_count == 0
        assert len(result.valid_records) == 2
        assert len(result.errors) == 0
    
    def test_parse_with_blood_group_normalization(self):
        """Test parsing normalizes blood groups."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A Positive,RBC,5,{future_date},{today}
R002,H001,b-,Platelets,3,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 2
        assert result.valid_records[0].blood_group == BloodGroup.A_POS
        assert result.valid_records[1].blood_group == BloodGroup.B_NEG
    
    def test_parse_with_invalid_blood_group(self):
        """Test parsing rejects invalid blood groups."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,XYZ,RBC,5,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert len(result.errors) == 1
        assert result.errors[0]["field"] == "blood_group"
    
    def test_parse_with_invalid_component(self):
        """Test parsing rejects invalid components."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,InvalidComponent,5,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert result.errors[0]["field"] == "component"
    
    def test_parse_with_negative_units(self):
        """Test parsing rejects negative units."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,-5,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert result.errors[0]["field"] == "units"
    
    def test_parse_with_zero_units(self):
        """Test parsing rejects zero units."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,0,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert result.errors[0]["field"] == "units"
    
    def test_parse_with_invalid_date_format(self):
        """Test parsing rejects invalid date formats."""
        csv_content = """record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,invalid-date,2024-11-01"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert result.errors[0]["field"] == "unit_expiry_date"
    
    def test_parse_with_expiry_before_collection(self):
        """Test parsing rejects expiry date before collection date."""
        today = date.today()
        past_date = today - timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,{past_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert result.error_count == 1
        assert result.errors[0]["field"] == "unit_expiry_date"
    
    def test_parse_with_duplicates(self):
        """Test parsing detects and rejects duplicates."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,{future_date},{today}
R001,H001,B+,RBC,3,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 0
        assert len(result.duplicates) == 1
        assert "R001" in result.duplicates
    
    def test_parse_mixed_valid_and_invalid(self):
        """Test parsing handles mix of valid and invalid records."""
        today = date.today()
        future_date = today + timedelta(days=30)
        
        csv_content = f"""record_id,hospital_id,blood_group,component,units,unit_expiry_date,collection_date
R001,H001,A+,RBC,5,{future_date},{today}
R002,H001,XYZ,RBC,3,{future_date},{today}
R003,H001,B+,Platelets,2,{future_date},{today}"""
        
        result = self.service.parse_csv(csv_content)
        
        assert result.success_count == 2
        assert result.error_count == 1
        assert len(result.valid_records) == 2
        assert len(result.errors) == 1
