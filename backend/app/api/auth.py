"""Authentication API endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.repositories.user import UserRepository
from app.utils.auth import verify_password, create_access_token, decode_access_token

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    user_id: str
    role: str


@router.post("/login", response_model=TokenResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    
    Args:
        request: Login credentials
        db: Database session
        
    Returns:
        Access token and user info
    """
    user_repo = UserRepository(db)
    user = user_repo.get_by_username(request.username)
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.user_id, "role": user.role}
    )
    
    return TokenResponse(
        access_token=access_token,
        user_id=user.user_id,
        role=user.role
    )


@router.post("/register")
def register(
    username: str,
    password: str,
    role: str = "staff",
    hospital_id: str = None,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Args:
        username: Username
        password: Password
        role: User role (staff or admin)
        hospital_id: Optional hospital ID
        db: Database session
        
    Returns:
        Created user info
    """
    user_repo = UserRepository(db)
    
    # Check if user exists
    existing = user_repo.get_by_username(username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )
    
    # Create user
    user = user_repo.create(username, password, role, hospital_id)
    
    return {
        "success": True,
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role
    }


@router.get("/me")
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user.
    
    Args:
        credentials: JWT token
        db: Database session
        
    Returns:
        Current user info
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "hospital_id": user.hospital_id
    }
