"""
Service layer for article summarization using LLMs.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.article import Article, ArticleStatus
from app.models.summary import Summary, SummaryStyle
from app.core.database import get_db


class SummarizationService:
    """Service for generating article summaries using LLMs."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def summarize_article(
        self, 
        article: Article, 
        style: SummaryStyle = SummaryStyle.NEWS_ANCHOR,
        model: str = "gpt-4o-mini"
    ) -> Summary:
        """Generate a summary for a single article."""
        # TODO: Implement LLM-based summarization
        summary_content = f"[Summary of: {article.title}]"
        
        summary = Summary(
            article_id=article.id,
            style=style,
            content=summary_content,
            model_used=model,
            tokens_used=0
        )
        self.db.add(summary)
        
        # Update article status
        article.status = ArticleStatus.SUMMARIZED
        self.db.commit()
        self.db.refresh(summary)
        
        return summary
    
    def summarize_batch(
        self, 
        articles: List[Article], 
        style: SummaryStyle = SummaryStyle.NEWS_ANCHOR,
        model: str = "gpt-4o-mini"
    ) -> List[Summary]:
        """Generate summaries for multiple articles."""
        summaries = []
        for article in articles:
            if article.status != ArticleStatus.SUMMARIZED:
                summary = self.summarize_article(article, style, model)
                summaries.append(summary)
        return summaries
    
    def get_latest_summaries(self, limit: int = 10) -> List[Summary]:
        """Get the most recent summaries."""
        return self.db.query(Summary).order_by(
            Summary.created_at.desc()
        ).limit(limit).all()