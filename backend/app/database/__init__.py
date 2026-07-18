"""
Database package for AI News Broadcaster.
Handles database connections and model definitions.
"""

from .init_db import Base, get_db, init_db

__all__ = ["Base", "get_db", "init_db"]