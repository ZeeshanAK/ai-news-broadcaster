"""
Article Deduplication Module
Removes duplicate articles from ingestion results.
"""
from typing import List, Dict, Optional
from hashlib import sha256


class Deduplicator:
    """Removes duplicate articles."""
    
    def __init__(self):
        self.seen_urls = set()
        self.seen_titles = set()
    
    def _hash_content(self, content: str) -> str:
        """Generate a hash of content."""
        return sha256(content.encode()).hexdigest()
    
    def deduplicate_by_url(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove articles with duplicate URLs.
        
        Args:
            articles: List of article dictionaries
        
        Returns:
            Deduplicated list
        """
        unique = []
        for article in articles:
            url = article.get('url')
            if url and url not in self.seen_urls:
                self.seen_urls.add(url)
                unique.append(article)
        return unique
    
    def deduplicate_by_title(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove articles with duplicate titles.
        
        Args:
            articles: List of article dictionaries
        
        Returns:
            Deduplicated list
        """
        unique = []
        for article in articles:
            title = article.get('title', '').strip()
            title_hash = self._hash_content(title)
            if title_hash not in self.seen_titles:
                self.seen_titles.add(title_hash)
                unique.append(article)
        return unique