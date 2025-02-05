from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.player import PlayerCreate, PlayerUpdate, PlayerInDB
from ....models.player import Player

router = APIRouter()

@router.get("/", response_model=List[PlayerInDB])
def get_players(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    players = db.query(Player).offset(skip).limit(limit).all()
    return players

@router.post("/", response_model=PlayerInDB)
def create_player(
    player: PlayerCreate,
    db: Session = Depends(get_db)
):
    db_player = Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

@router.get("/{player_id}", response_model=PlayerInDB)
def get_player(
    player_id: int,
    db: Session = Depends(get_db)
):
    player = db.query(Player).filter(Player.id == player_id).first()
    if player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден")
    return player

@router.put("/{player_id}", response_model=PlayerInDB)
def update_player(
    player_id: int,
    player: PlayerUpdate,
    db: Session = Depends(get_db)
):
    db_player = db.query(Player).filter(Player.id == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail="Игрок не найден")
    
    for field, value in player.model_dump(exclude_unset=True).items():
        setattr(db_player, field, value)
    
    db.commit()
    db.refresh(db_player)
    return db_player 