from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.game import GameCreate, GameUpdate, Game
from ....models.game import Game as GameModel

router = APIRouter()

@router.get("/", response_model=List[Game])
def get_games(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    games = db.query(GameModel).offset(skip).limit(limit).all()
    return games

@router.post("/", response_model=Game)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db)
):
    db_game = GameModel(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/{game_id}", response_model=Game)
def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game

@router.put("/{game_id}", response_model=Game)
def update_game(
    game_id: int,
    game: GameUpdate,
    db: Session = Depends(get_db)
):
    db_game = db.query(GameModel).filter(GameModel.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    for field, value in game.model_dump(exclude_unset=True).items():
        setattr(db_game, field, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game 