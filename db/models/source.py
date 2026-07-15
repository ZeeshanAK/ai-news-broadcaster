"""
Database source model.
Represents news sources (RSS feeds, APIs, etc.).
"""
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    RSS = "rss"
    API = "api"
    SCRAPER = "scraper"


class Source:
    """
    Source model placeholder.
    Full implementation in backend/app/models/source.py
    """
    
    # Fields
    id: int
    name: str
    url: str
    type: SourceType
    category: str
    language: str
    is_active: bool
    fetch_interval_minutes: int
    last_fetched_at: datetime
    last_error: str
    config: str
    created_at: datetime
    updated_at: datetime