from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class BroadcastStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING_AUDIO = "generating_audio"
    READY = "ready"
    PUBLISHED = "published"
    FAILED = "failed"


class Broadcast(Base):
    __tablename__ = "broadcasts"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    summary_id = Column(Integer, ForeignKey("summaries.id", ondelete="SET NULL"), nullable=True, index=True)
    title = Column(String(500), nullable=False)
    script = Column(Text, nullable=False)
    audio_url = Column(String(1000), nullable=True)
    audio_duration_seconds = Column(Integer, nullable=True)
    voice_id = Column(String(100), nullable=True)
    status = Column(SQLEnum(BroadcastStatus), default=BroadcastStatus.PENDING, nullable=False, index=True)
    error_message = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    article = relationship("Article", back_populates="broadcasts")
    summary = relationship("Summary", back_populates="broadcasts")