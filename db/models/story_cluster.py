"""
Database story cluster model.
Represents grouped related articles (stories).
"""
from datetime import datetime


class StoryCluster:
    """
    Story cluster model placeholder.
    Represents a grouping of related articles.
    """
    
    # Fields
    id: int
    name: str
    description: str
    article_ids: list
    created_at: datetime
    updated_at: datetime