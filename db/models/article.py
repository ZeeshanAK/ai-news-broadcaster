"""
Database article model.
Represents fetched news articles.
"""
from datetime import datetime
from enum import Enum


class ArticleStatus(str, Enum):
    NEW = "new"
    PROCESSED = "processed"
    SUMMARIZED = "summarized"
    BROADCASTED = "broadcasted"
    ARCHIVED = "archived"


class Article:
    """
    Article model placeholder.
    Full implementation in backend/app/models/article.py
    """
    
    # Fields
    id: int
    source_id: int
    title: str
    url: str
    content: str
    summary: str
    category: str
    author: str
    published_at: datetime
    fetched_at: datetime
    status: ArticleStatus
    language: str