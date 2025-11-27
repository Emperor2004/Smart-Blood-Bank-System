"""Initialize the database with migrations."""
import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from alembic.config import Config
from alembic import command


def init_database():
    """Run database migrations."""
    print("Initializing database...")
    
    # Get alembic config
    alembic_ini = backend_path / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini))
    
    # Set script location
    alembic_cfg.set_main_option("script_location", str(backend_path / "alembic"))
    
    # Run migrations
    try:
        command.upgrade(alembic_cfg, "head")
        print("✓ Database initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
