"""
Database user settings model.
Stores user preferences and configurations including broadcast timing.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class UserSettings(Base):
    """
    User settings model for storing broadcast timing preferences and other settings.
    """
    
    __tablename__ = "user_settings"
    
    # Fields
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    key = Column(String(100), unique=True, nullable=False, index=True)
    value = Column(String, nullable=False)
    category = Column(String(50), nullable=True, index=True)
    description = Column(String, nullable=True)
    is_secret = Column(Integer, default=0, nullable=False)  # Using Integer instead of Boolean for compatibility
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Broadcast timing preferences
    morning_broadcast_hour = Column(Integer, nullable=True)
    noon_broadcast_hour = Column(Integer, nullable=True)
    evening_broadcast_hour = Column(Integer, nullable=True)