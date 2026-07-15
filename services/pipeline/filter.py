"""
Article Filtering Module
Filters and prioritizes articles based on relevance and category.
"""
from typing import List, Optional, Callable
from enum import Enum


class FilterCriteria(str, Enum):
    CATEGORY = "category"
    KEYWORDS = "keywords"
    SOURCE = "source"
    LANGUAGE = "language"


class ArticleFilter:
    """Filters articles based on criteria."""
    
    def __init__(self):
        self.filters: List[Callable] = []
    
    def add_category_filter(self, categories: List[str]):
        """Add a category filter."""
        def filter_func(article):
            return article.get('category') in categories
        self.filters.append(filter_func)
    
    def add_keyword_filter(self, keywords: List[str]):
        """Add a keyword filter."""
        def filter_func(article):
            text = (article.get('title', '') + ' ' + article.get('content', '')).lower()
            return any(keyword.lower() in text for keyword in keywords)
        self.filters.append(filter_func)
    
    def apply_filters(self, articles: List[dict]) -> List[dict]:
        """Apply all filters to articles."""
        filtered = articles
        for filter_func in self.filters:
            filtered = [a for a in filtered if filter_func(a)]
        return filtered