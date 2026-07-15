from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class ArticleStatus(str, enum.Enum):
    NEW = "new"
    PROCESSED = "processed"
    SUMMARIZED = "summarized"
    BROADCASTED = "broadcasted"
    ARCHIVED = "archived"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    title = Column(String(500), nullable=False)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    author = Column(String(200), nullable=True)
    published_at = Column(DateTime, nullable=True, index=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    status = Column(SQLEnum(ArticleStatus), default=ArticleStatus.NEW, nullable=False, index=True)
    language = Column(String(10), default="en", nullable=False)
    
    source = relationship("Source", back_populates="articles")
    summaries = relationship("Summary", back_populates="article", cascade="all, delete-orphan")
    broadcasts = relationship("Broadcast", back_populates="article", cascade="all, delete-orphan")