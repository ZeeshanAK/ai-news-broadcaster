from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.summary import Summary, SummaryStyle
from app.schemas import (
    SummaryCreate, SummaryUpdate, SummaryResponse, PaginatedResponse
)

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.get("/", response_model=PaginatedResponse)
def list_summaries(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    style: Optional[SummaryStyle] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Summary)
    if style:
        query = query.filter(Summary.style == style)
    total = query.count()
    summaries = query.order_by(Summary.created_at.desc()).offset(skip).limit(limit).all()
    return {
        "items": summaries,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit
    }


@router.get("/{summary_id}", response_model=SummaryResponse)
def get_summary(summary_id: int, db: Session = Depends(get_db)):
    summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.post("/", response_model=SummaryResponse, status_code=201)
def create_summary(summary: SummaryCreate, db: Session = Depends(get_db)):
    db_summary = Summary(**summary.model_dump())
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary


@router.patch("/{summary_id}", response_model=SummaryResponse)
def update_summary(summary_id: int, summary: SummaryUpdate, db: Session = Depends(get_db)):
    db_summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not db_summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    for key, value in summary.model_dump(exclude_unset=True).items():
        setattr(db_summary, key, value)
    db.commit()
    db.refresh(db_summary)
    return db_summary


@router.delete("/{summary_id}", status_code=204)
def delete_summary(summary_id: int, db: Session = Depends(get_db)):
    db_summary = db.query(Summary).filter(Summary.id == summary_id).first()
    if not db_summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    db.delete(db_summary)
    db.commit()
    return None