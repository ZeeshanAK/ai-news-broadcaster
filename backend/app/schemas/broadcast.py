from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.models.broadcast import BroadcastStatus


class BroadcastBase(BaseModel):
    article_id: int
    summary_id: Optional[int] = None
    title: str
    script: str
    audio_url: Optional[str] = None
    audio_duration_seconds: Optional[int] = None
    voice_id: Optional[str] = None
    status: BroadcastStatus = BroadcastStatus.PENDING
    error_message: Optional[str] = None
    published_at: Optional[datetime] = None


class BroadcastCreate(BroadcastBase):
    pass


class BroadcastUpdate(BroadcastBase):
    pass


class BroadcastResponse(BroadcastBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True