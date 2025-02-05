from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....core.database import get_db
from ....schemas.leaderboard import LeaderboardCreate, LeaderboardUpdate, LeaderboardInDB, LeaderboardBase
from ....models.leaderboard import Leaderboard

router = APIRouter()

@router.get("/", response_model=List[LeaderboardInDB])
def get_leaderboard(
    db: Session = Depends(get_db)
):
    return db.query(Leaderboard).all()

@router.post("/", response_model=LeaderboardInDB)
def create_leaderboard(
    leaderboard: LeaderboardCreate,
    db: Session = Depends(get_db)
):
    
    new_command = Leaderboard(**leaderboard.model_dump())
    db.add(new_command)
    db.commit()
    db.refresh(new_command)
    return new_command

@router.delete("/{leaderboard_id}", response_model=LeaderboardInDB)
def delete_leaderboard(
    leaderboard_id: int,
    db: Session = Depends(get_db)
):
    leaderboard = db.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).first()
    db.delete(leaderboard)
    db.commit()
    return leaderboard

@router.put("/{leaderboard_id}", response_model=LeaderboardInDB)
def update_leaderboard(
    leaderboard_id: int,
    leaderboard: LeaderboardUpdate,
    db: Session = Depends(get_db)
):
    leaderboard_to_update = db.query(Leaderboard).filter(Leaderboard.id == leaderboard_id).first()
    for k, v in leaderboard.model_dump().items():
        if v is not None:
            setattr(leaderboard_to_update, k, v)
    db.commit()
    return leaderboard_to_update
