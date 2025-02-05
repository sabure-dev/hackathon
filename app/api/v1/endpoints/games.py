from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ....core.database import get_db
from ....schemas.game import GameCreate, GameUpdate, GameInDB
from ....schemas.player import GenderType
from ....models.game import Game
from ....models.team import Team

router = APIRouter()

@router.get("/", response_model=List[GameInDB])
def get_games(
    skip: int = 0,
    limit: int = 100,
    gender: Optional[GenderType] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    team_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Получить список игр с возможностью фильтрации
    """
    query = db.query(Game)
    if gender:
        query = query.filter(Game.gender == gender)
    if start_date:
        query = query.filter(Game.date_time >= start_date)
    if end_date:
        query = query.filter(Game.date_time <= end_date)
    if team_name:
        query = query.filter(Game.team_name == team_name)
    
    query = query.order_by(Game.date_time.desc())
    games = query.offset(skip).limit(limit).all()
    return games

@router.get("/upcoming", response_model=List[GameInDB])
def get_upcoming_games(
    limit: int = 10,
    gender: GenderType = None,
    db: Session = Depends(get_db)
):
    """
    Получить список предстоящих игр
    """
    query = db.query(Game).filter(Game.date_time >= datetime.now())
    if gender:
        query = query.filter(Game.gender == gender)
    query = query.order_by(Game.date_time.asc())
    games = query.limit(limit).all()
    return games

@router.get("/results", response_model=List[GameInDB])
def get_game_results(
    skip: int = 0,
    limit: int = 100,
    gender: GenderType = None,
    db: Session = Depends(get_db)
):
    """
    Получить результаты прошедших игр
    """
    query = db.query(Game).filter(
        Game.date_time < datetime.now(),
        Game.score_black_bears.isnot(None),
        Game.score_opponent.isnot(None)
    )
    if gender:
        query = query.filter(Game.gender == gender)
    query = query.order_by(Game.date_time.desc())
    games = query.offset(skip).limit(limit).all()
    return games

@router.post("/", response_model=GameInDB)
def create_game(
    game: GameCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую игру
    """
    # Проверяем существование команды
    team = db.query(Team).filter(Team.name == game.team_name).first()
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    
    if team.gender != game.gender:
        raise HTTPException(
            status_code=400,
            detail="Пол команды не соответствует полу, указанному для игры"
        )
    
    db_game = Game(**game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.get("/{game_id}", response_model=GameInDB)
def get_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить информацию о конкретной игре
    """
    game = db.query(Game).filter(Game.id == game_id).first()
    if game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return game

@router.put("/{game_id}", response_model=GameInDB)
def update_game(
    game_id: int,
    game: GameUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить информацию об игре
    """
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    # Если меняется команда-оппонент, проверяем её существование и пол
    if game.team_name is not None:
        team = db.query(Team).filter(Team.name == game.team_name).first()
        if not team:
            raise HTTPException(status_code=404, detail="Команда не найдена")
        
        game_gender = game.gender if game.gender is not None else db_game.gender
        if team.gender != game_gender:
            raise HTTPException(
                status_code=400,
                detail="Пол команды не соответствует полу, указанному для игры"
            )
    
    for field, value in game.model_dump(exclude_unset=True).items():
        setattr(db_game, field, value)
    
    db.commit()
    db.refresh(db_game)
    return db_game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить игру
    """
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if db_game is None:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    
    db.delete(db_game)
    db.commit()
    return {"message": "Игра успешно удалена"} 