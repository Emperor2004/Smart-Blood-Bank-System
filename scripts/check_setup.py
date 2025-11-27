"""Check if the development environment is properly set up."""
import sys
import os
from pathlib import Path


def check_python_version():
    """Check Python version."""
    version = sys.version_info
    if version >= (3, 10):
        print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} (3.10+ required)")
        return False


def check_dependencies():
    """Check if required packages are installed."""
    required = [
        "fastapi",
        "sqlalchemy",
        "alembic",
        "pandas",
        "prophet",
        "hypothesis",
        "pytest",
        "pydantic",
        "uvicorn"
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (not installed)")
            missing.append(package)
    
    return len(missing) == 0


def check_env_file():
    """Check if .env file exists."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        print("✓ .env file exists")
        return True
    else:
        print("✗ .env file not found (copy from .env.example)")
        return False


def check_directory_structure():
    """Check if required directories exist."""
    base_path = Path(__file__).parent.parent
    required_dirs = [
        "backend/app/models",
        "backend/app/services",
        "backend/app/api",
        "backend/app/repositories",
        "backend/alembic",
        "tests",
        "scripts",
        "docker"
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        full_path = base_path / dir_path
        if full_path.exists():
            print(f"✓ {dir_path}")
        else:
            print(f"✗ {dir_path} (missing)")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks."""
    print("=" * 60)
    print("Smart Blood Bank - Environment Setup Check")
    print("=" * 60)
    
    print("\n1. Python Version:")
    python_ok = check_python_version()
    
    print("\n2. Python Dependencies:")
    deps_ok = check_dependencies()
    
    print("\n3. Environment Configuration:")
    env_ok = check_env_file()
    
    print("\n4. Directory Structure:")
    dirs_ok = check_directory_structure()
    
    print("\n" + "=" * 60)
    if python_ok and deps_ok and env_ok and dirs_ok:
        print("✓ All checks passed! Environment is ready.")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        if not deps_ok:
            print("\nTo install dependencies, run:")
            print("  cd backend && pip install -r requirements.txt")
        if not env_ok:
            print("\nTo create .env file, run:")
            print("  cp .env.example .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
