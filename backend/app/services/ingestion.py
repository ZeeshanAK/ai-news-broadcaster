"""
Service layer for article ingestion and processing.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.article import Article, ArticleStatus
from app.models.source import Source, SourceType
from app.core.database import get_db


class IngestionService:
    """Service for fetching and ingesting articles from sources."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def fetch_from_rss(self, source: Source) -> List[Article]:
        """Fetch articles from an RSS feed source."""
        # TODO: Implement RSS fetching logic
        return []
    
    def fetch_from_api(self, source: Source) -> List[Article]:
        """Fetch articles from an API source."""
        # TODO: Implement API fetching logic
        return []
    
    def fetch_from_scraper(self, source: Source) -> List[Article]:
        """Fetch articles using web scraping."""
        # TODO: Implement scraping logic
        return []
    
    def fetch_all_active_sources(self) -> List[Article]:
        """Fetch articles from all active sources."""
        sources = self.db.query(Source).filter(Source.is_active == True).all()
        all_articles = []
        for source in sources:
            if source.type == SourceType.RSS:
                articles = self.fetch_from_rss(source)
            elif source.type == SourceType.API:
                articles = self.fetch_from_api(source)
            elif source.type == SourceType.SCRAPER:
                articles = self.fetch_from_scraper(source)
            else:
                continue
            
            for article in articles:
                article.source_id = source.id
                self.db.add(article)
            all_articles.extend(articles)
        
        self.db.commit()
        return all_articles
    
    def deduplicate_articles(self, articles: List[Article]) -> List[Article]:
        """Remove duplicate articles based on URL."""
        seen_urls = set()
        unique_articles = []
        for article in articles:
            if article.url not in seen_urls:
                seen_urls.add(article.url)
                unique_articles.append(article)
        return unique_articles