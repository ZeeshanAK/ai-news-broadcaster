from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.article import Article
from app.schemas import (
    ArticleCreate, ArticleUpdate, ArticleResponse, PaginatedResponse
)

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/", response_model=PaginatedResponse)
def list_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    source_id: Optional[int] = None,
    category: Optional[str] = None,
    is_processed: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Article)
    if source_id:
        query = query.filter(Article.source_id == source_id)
    if category:
        query = query.filter(Article.category == category)
    if is_processed is not None:
        query = query.filter(Article.is_processed == is_processed)
    
    total = query.count()
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[ArticleResponse.model_validate(a) for a in articles],
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse.model_validate(article)


@router.post("/", response_model=ArticleResponse, status_code=201)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    db_article = Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return ArticleResponse.model_validate(db_article)


@router.patch("/{article_id}", response_model=ArticleResponse)
def update_article(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in article.model_dump(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return ArticleResponse.model_validate(db_article)


@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(db_article)
    db.commit()
    return None