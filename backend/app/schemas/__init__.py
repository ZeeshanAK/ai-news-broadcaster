from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

from app.models.article import ArticleStatus
from app.models.source import SourceType
from app.models.summary import SummaryStyle
from app.models.broadcast import BroadcastStatus


class SourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    url: HttpUrl
    type: SourceType = SourceType.RSS
    category: Optional[str] = Field(None, max_length=100)
    language: str = Field(default="en", min_length=2, max_length=10)
    is_active: bool = True
    fetch_interval_minutes: int = Field(default=60, ge=1)
    config: Optional[str] = None


class SourceCreate(SourceBase):
    pass


class SourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[HttpUrl] = None
    type: Optional[SourceType] = None
    category: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, min_length=2, max_length=10)
    is_active: Optional[bool] = None
    fetch_interval_minutes: Optional[int] = Field(None, ge=1)
    config: Optional[str] = None


class SourceResponse(SourceBase):
    id: int
    last_fetched_at: Optional[datetime] = None
    last_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    url: HttpUrl
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=200)
    published_at: Optional[datetime] = None
    language: str = Field(default="en", min_length=2, max_length=10)


class ArticleCreate(ArticleBase):
    source_id: int


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    author: Optional[str] = Field(None, max_length=200)
    published_at: Optional[datetime] = None
    status: Optional[ArticleStatus] = None
    language: Optional[str] = Field(None, min_length=2, max_length=10)


class ArticleResponse(ArticleBase):
    id: int
    source_id: int
    status: ArticleStatus
    fetched_at: datetime
    source: Optional[SourceResponse] = None

    class Config:
        from_attributes = True


class SummaryBase(BaseModel):
    style: SummaryStyle = SummaryStyle.NEWS_ANCHOR
    content: str
    model_used: Optional[str] = Field(None, max_length=100)
    tokens_used: Optional[int] = None


class SummaryCreate(SummaryBase):
    article_id: int


class SummaryResponse(SummaryBase):
    id: int
    article_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BroadcastBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=500)
    script: str
    voice_id: Optional[str] = Field(None, max_length=100)


class BroadcastCreate(BroadcastBase):
    article_id: int
    summary_id: Optional[int] = None


class BroadcastUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    script: Optional[str] = None
    audio_url: Optional[HttpUrl] = None
    audio_duration_seconds: Optional[int] = None
    voice_id: Optional[str] = Field(None, max_length=100)
    status: Optional[BroadcastStatus] = None
    error_message: Optional[str] = None


class BroadcastResponse(BroadcastBase):
    id: int
    article_id: int
    summary_id: Optional[int] = None
    audio_url: Optional[str] = None
    audio_duration_seconds: Optional[int] = None
    status: BroadcastStatus
    error_message: Optional[str] = None
    published_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SettingsBase(BaseModel):
    key: str = Field(..., min_length=1, max_length=100)
    value: str
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    is_secret: bool = False


class SettingsCreate(SettingsBase):
    pass


class SettingsUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)
    is_secret: Optional[bool] = None


class SettingsResponse(SettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    items: List[BaseModel]
    total: int
    page: int
    page_size: int
    total_pages: int