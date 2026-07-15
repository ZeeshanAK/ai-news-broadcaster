"""
Summarizer Module
Orchestrates article summarization using LLM.
"""
from typing import List, Optional
from services.pipeline.llm_client import LLMClient


class Summarizer:
    """Orchestrates article summarization."""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def summarize(
        self, 
        article: dict,
        style: str = "news_anchor"
    ) -> dict:
        """
        Generate a summary for an article.
        
        Args:
            article: Article dictionary with 'content' key
            style: Summary style
        
        Returns:
            Dictionary with summary information
        """
        content = article.get('content', '')
        summary_text = self.llm_client.generate_summary(content, style)
        
        return {
            'article_id': article.get('id'),
            'summary': summary_text,
            'style': style,
            'model': 'gpt-4o-mini'
        }
    
    def summarize_batch(
        self, 
        articles: List[dict],
        style: str = "news_anchor"
    ) -> List[dict]:
        """
        Generate summaries for multiple articles.
        
        Args:
            articles: List of article dictionaries
            style: Summary style
        
        Returns:
            List of summary dictionaries
        """
        return [self.summarize(article, style) for article in articles]