"""Basic setup verification tests."""
import pytest


def test_python_version():
    """Verify Python version is 3.10 or higher."""
    import sys
    assert sys.version_info >= (3, 10), "Python 3.10+ required"


def test_imports():
    """Verify key dependencies can be imported."""
    try:
        import fastapi
        import sqlalchemy
        import pandas
        import hypothesis
        import pytest
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required dependency: {e}")


def test_config_loads():
    """Verify configuration can be loaded."""
    from backend.app.config import settings
    assert settings is not None
    assert settings.environment in ["development", "production", "testing"]
