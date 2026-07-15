from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.settings import Settings
from app.schemas import (
    SettingsCreate, SettingsUpdate, SettingsResponse, PaginatedResponse
)

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("/", response_model=PaginatedResponse)
def list_settings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Settings)
    if category:
        query = query.filter(Settings.category == category)
    total = query.count()
    settings = query.offset(skip).limit(limit).all()
    return {
        "items": settings,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit
    }


@router.get("/{key}", response_model=SettingsResponse)
def get_setting(key: str, db: Session = Depends(get_db)):
    setting = db.query(Settings).filter(Settings.key == key).first()
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.post("/", response_model=SettingsResponse, status_code=201)
def create_setting(setting: SettingsCreate, db: Session = Depends(get_db)):
    existing = db.query(Settings).filter(Settings.key == setting.key).first()
    if existing:
        raise HTTPException(status_code=400, detail="Setting with this key already exists")
    db_setting = Settings(**setting.model_dump())
    db.add(db_setting)
    db.commit()
    db.refresh(db_setting)
    return db_setting


@router.patch("/{key}", response_model=SettingsResponse)
def update_setting(key: str, setting: SettingsUpdate, db: Session = Depends(get_db)):
    db_setting = db.query(Settings).filter(Settings.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    for k, value in setting.model_dump(exclude_unset=True).items():
        setattr(db_setting, k, value)
    db_setting.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_setting)
    return db_setting


@router.delete("/{key}", status_code=204)
def delete_setting(key: str, db: Session = Depends(get_db)):
    db_setting = db.query(Settings).filter(Settings.key == key).first()
    if not db_setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    db.delete(db_setting)
    db.commit()
    return None