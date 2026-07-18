from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.broadcast import Broadcast, BroadcastStatus
from app.schemas import (
    BroadcastCreate, BroadcastUpdate, BroadcastResponse, PaginatedResponse
)
from app.services.audio_storage import audio_storage_service

router = APIRouter(prefix="/broadcasts", tags=["broadcasts"])


@router.get("/", response_model=PaginatedResponse)
def list_broadcasts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[BroadcastStatus] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Broadcast)
    if status:
        query = query.filter(Broadcast.status == status)
    total = query.count()
    broadcasts = query.order_by(Broadcast.created_at.desc()).offset(skip).limit(limit).all()
    return {
        "items": broadcasts,
        "total": total,
        "page": skip // limit + 1,
        "page_size": limit,
        "total_pages": (total + limit - 1) // limit
    }


@router.get("/{broadcast_id}", response_model=BroadcastResponse)
def get_broadcast(broadcast_id: int, db: Session = Depends(get_db)):
    broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    return broadcast


@router.post("/", response_model=BroadcastResponse, status_code=201)
def create_broadcast(broadcast: BroadcastCreate, db: Session = Depends(get_db)):
    db_broadcast = Broadcast(**broadcast.model_dump())
    db.add(db_broadcast)
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


@router.patch("/{broadcast_id}", response_model=BroadcastResponse)
def update_broadcast(broadcast_id: int, broadcast: BroadcastUpdate, db: Session = Depends(get_db)):
    db_broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not db_broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    for key, value in broadcast.model_dump(exclude_unset=True).items():
        setattr(db_broadcast, key, value)
    db_broadcast.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


@router.post("/{broadcast_id}/audio", response_model=BroadcastResponse)
async def upload_audio(
    broadcast_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Get the broadcast
    db_broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not db_broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    
    # Save audio file
    audio_url = await audio_storage_service.save_audio_file(file, broadcast_id)
    
    # Update broadcast with audio URL
    db_broadcast.audio_url = audio_url
    db_broadcast.status = BroadcastStatus.READY
    
    db.commit()
    db.refresh(db_broadcast)
    return db_broadcast


@router.delete("/{broadcast_id}", status_code=204)
def delete_broadcast(broadcast_id: int, db: Session = Depends(get_db)):
    db_broadcast = db.query(Broadcast).filter(Broadcast.id == broadcast_id).first()
    if not db_broadcast:
        raise HTTPException(status_code=404, detail="Broadcast not found")
    db.delete(db_broadcast)
    db.commit()
    return None