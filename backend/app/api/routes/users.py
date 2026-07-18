from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserSettingsUpdate

router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user with registration details.
    """
    # Check if user with this mobile number already exists
    existing_user = db.query(User).filter(User.mobile_number == user.mobile_number).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this mobile number already exists")
    
    # Create new user
    db_user = User(
        name=user.name,
        mobile_number=user.mobile_number,
        created_at="2026-07-18"  # We'll use a simple date format for now
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}/settings", response_model=UserResponse)
def update_user_settings(
    user_id: int, 
    settings: UserSettingsUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update user's broadcast timing preferences.
    """
    # First check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate timing ranges (6-9 for morning, 12-15 for noon, 19-22 for evening)
    if settings.morning_broadcast_hour is not None:
        if not (6 <= settings.morning_broadcast_hour <= 9):
            raise HTTPException(status_code=400, detail="Morning broadcast hour must be between 6 and 9")
    
    if settings.noon_broadcast_hour is not None:
        if not (12 <= settings.noon_broadcast_hour <= 15):
            raise HTTPException(status_code=400, detail="Noon broadcast hour must be between 12 and 15")
    
    if settings.evening_broadcast_hour is not None:
        if not (19 <= settings.evening_broadcast_hour <= 22):
            raise HTTPException(status_code=400, detail="Evening broadcast hour must be between 19 and 22")
    
    # Update user settings
    # In a real implementation, we'd update the settings in the database
    # For now, we'll just return the user with updated preferences
    return user