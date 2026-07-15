from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.source import Source, SourceType
from app.schemas import (
    SourceCreate, SourceUpdate, SourceResponse, PaginatedResponse
)

router = APIRouter(prefix="/sources", tags=["sources"])


@router.get("/", response_model=PaginatedResponse)
def list_sources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    is_active: Optional[bool] = None,
    category: Optional[str] = None,
    source_type: Optional[SourceType] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Source)
    if is_active is not None:
        query = query.filter(Source.is_active == is_active)
    if category:
        query = query.filter(Source.category == category)
    if source_type:
        query = query.filter(Source.type == source_type)
    
    total = query.count()
    sources = query.offset(skip).limit(limit).all()
    
    return PaginatedResponse(
        items=[SourceResponse.model_validate(s) for s in sources],
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=(total + limit - 1) // limit
    )


@router.get("/{source_id}", response_model=SourceResponse)
def get_source(source_id: int, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    return SourceResponse.model_validate(source)


@router.post("/", response_model=SourceResponse, status_code=201)
def create_source(source: SourceCreate, db: Session = Depends(get_db)):
    existing = db.query(Source).filter(Source.name == source.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source with this name already exists")
    
    db_source = Source(**source.model_dump())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return SourceResponse.model_validate(db_source)


@router.patch("/{source_id}", response_model=SourceResponse)
def update_source(source_id: int, source: SourceUpdate, db: Session = Depends(get_db)):
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    
    for key, value in source.model_dump(exclude_unset=True).items():
        setattr(db_source, key, value)
    
    db_source.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_source)
    return SourceResponse.model_validate(db_source)


@router.delete("/{source_id}", status_code=204)
def delete_source(source_id: int, db: Session = Depends(get_db)):
    db_source = db.query(Source).filter(Source.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(db_source)
    db.commit()
    return None


@router.post("/{source_id}/fetch", response_model=dict)
def trigger_fetch(source_id: int, db: Session = Depends(get_db)):
    source = db.query(Source).filter(Source.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    if not source.is_active:
        raise HTTPException(status_code=400, detail="Source is not active")
    
    # TODO: Trigger actual fetch job
    source.last_fetched_at = datetime.utcnow()
    db.commit()
    return {"message": "Fetch triggered", "source_id": source_id}