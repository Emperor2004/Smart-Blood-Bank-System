"""User repository for database operations."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.auth import hash_password


class UserRepository:
    """Repository for user CRUD operations."""
    
    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db
    
    def create(self, username: str, password: str, role: str, hospital_id: Optional[str] = None) -> User:
        """Create a new user."""
        hashed_password = hash_password(password)
        
        db_user = User(
            user_id=username,  # Using username as user_id for simplicity
            username=username,
            password_hash=hashed_password,
            role=role,
            hospital_id=hospital_id
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.user_id == user_id).first()
