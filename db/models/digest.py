"""
Database digest model.
Represents digest messages sent to users.
"""
from datetime import datetime


class Digest:
    """
    Digest model placeholder.
    Represents a news digest or broadcast.
    """
    
    # Fields
    id: int
    title: str
    content: str
    articles: list
    created_at: datetime
    sent_at: datetime