from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class SourceType(str, enum.Enum):
    RSS = "rss"
    API = "api"
    SCRAPER = "scraper"


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    url = Column(String(1000), nullable=False)
    type = Column(SQLEnum(SourceType), default=SourceType.RSS, nullable=False)
    category = Column(String(100), nullable=True, index=True)
    language = Column(String(10), default="en", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    fetch_interval_minutes = Column(Integer, default=60, nullable=False)
    last_fetched_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    config = Column(Text, nullable=True)  # JSON config for API keys, selectors, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")