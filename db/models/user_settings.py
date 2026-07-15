"""
Database user settings model.
Stores user preferences and configurations.
"""
from datetime import datetime


class UserSettings:
    """
    User settings model placeholder.
    Stores application and user-specific settings.
    """
    
    # Fields
    id: int
    key: str
    value: str
    category: str
    description: str
    is_secret: bool
    created_at: datetime
    updated_at: datetime