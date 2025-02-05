from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....core.database import get_db
from ....schemas.player import PlayerCreate, PlayerUpdate, PlayerInDB, GenderType
from ....models.player import Player

router = APIRouter()

@router.get("/", response_model=List[PlayerInDB])
def get_players(
    skip: int = 0,
    limit: int = 100,
    gender: Optional[GenderType] = None,
    search: Optional[str] = None,
    min_games: Optional[int] = None,
    sort_by: str = Query(
        "name",
        description="Сортировка: name, points, rebounds, assists, steals, blocks"
    ),
    db: Session = Depends(get_db)
):
    """
    Получить список игроков с возможностью фильтрации и сортировки.
    
    Параметры:
    - gender: фильтр по полу (male/female)
    - search: поиск по имени/фамилии
    - min_games: минимальное количество сыгранных игр
    - sort_by: поле для сортировки (name, points, rebounds, assists, steals, blocks)
    """
    query = db.query(Player)
    
    # Применяем фильтры
    if gender:
        query = query.filter(Player.gender == gender)
    if search:
        search = f"%{search}%"
        query = query.filter(
            (Player.first_name.ilike(search)) | 
            (Player.last_name.ilike(search))
        )
    if min_games:
        query = query.filter(Player.games_played >= min_games)

    # Определяем сортировку
    sort_field = {
        "name": (Player.last_name.asc(), Player.first_name.asc()),
        "points": Player.total_points.desc(),
        "rebounds": Player.total_rebounds.desc(),
        "assists": Player.total_assists.desc(),
        "steals": Player.total_steals.desc(),
        "blocks": Player.total_blocks.desc()
    }.get(sort_by, (Player.last_name.asc(), Player.first_name.asc()))

    # Применяем сортировку
    if isinstance(sort_field, tuple):
        query = query.order_by(*sort_field)
    else:
        query = query.order_by(sort_field)

    players = query.offset(skip).limit(limit).all()
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