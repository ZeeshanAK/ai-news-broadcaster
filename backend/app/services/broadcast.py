"""
Service layer for broadcast scheduling and management.
"""
from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.broadcast import Broadcast, BroadcastStatus
from app.models.article import Article, ArticleStatus
from app.models.summary import Summary
from app.core.database import get_db


class BroadcastService:
    """Service for managing broadcasts and scheduling."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_broadcast_from_summary(
        self, 
        summary: Summary, 
        title: Optional[str] = None
    ) -> Broadcast:
        """Create a broadcast from a summary."""
        article = summary.article
        broadcast_title = title or f"News Brief: {article.title}"
        
        broadcast = Broadcast(
            article_id=article.id,
            summary_id=summary.id,
            title=broadcast_title,
            script=summary.content,
            status=BroadcastStatus.PENDING
        )
        self.db.add(broadcast)
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast
    
    def schedule_broadcast(self, broadcast_id: int, scheduled_at: datetime) -> Broadcast:
        """Schedule a broadcast for a specific time."""
        broadcast = self.db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        if not broadcast:
            raise ValueError("Broadcast not found")
        
        broadcast.scheduled_at = scheduled_at
        broadcast.status = BroadcastStatus.SCHEDULED
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast
    
    def get_pending_broadcasts(self, limit: int = 10) -> List[Broadcast]:
        """Get broadcasts ready to be processed."""
        return self.db.query(Broadcast).filter(
            Broadcast.status == BroadcastStatus.PENDING
        ).limit(limit).all()
    
    def get_scheduled_broadcasts(self, before: datetime = None) -> List[Broadcast]:
        """Get broadcasts scheduled for publishing."""
        if before is None:
            before = datetime.utcnow()
        return self.db.query(Broadcast).filter(
            Broadcast.status == BroadcastStatus.SCHEDULED,
            Broadcast.scheduled_at <= before
        ).all()
    
    def publish_broadcast(self, broadcast_id: int) -> Broadcast:
        """Mark a broadcast as published."""
        broadcast = self.db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
        if not broadcast:
            raise ValueError("Broadcast not found")
        
        broadcast.status = BroadcastStatus.PUBLISHED
        broadcast.published_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(broadcast)
        return broadcast