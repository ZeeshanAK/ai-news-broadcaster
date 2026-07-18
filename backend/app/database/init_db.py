"""
Database initialization module.
Handles creation of tables and database setup for both SQLite and PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models import user, broadcast, source, article, summary

# Create database engine based on environment
if settings.DATABASE_URL.startswith("sqlite"):
    # For SQLite (local development)
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For PostgreSQL (Supabase deployment)
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize the database with all models."""
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")