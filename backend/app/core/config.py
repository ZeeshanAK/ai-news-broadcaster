import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "AI News Broadcaster"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_news.db")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # Scheduler
    FETCH_INTERVAL_MINUTES: int = int(os.getenv("FETCH_INTERVAL_MINUTES", "30"))
    SUMMARY_INTERVAL_MINUTES: int = int(os.getenv("SUMMARY_INTERVAL_MINUTES", "60"))
    BROADCAST_INTERVAL_MINUTES: int = int(os.getenv("BROADCAST_INTERVAL_MINUTES", "120"))
    
    # TTS
    TTS_PROVIDER: str = os.getenv("TTS_PROVIDER", "openai")
    TTS_VOICE: str = os.getenv("TTS_VOICE", "alloy")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()