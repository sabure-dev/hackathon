from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ....core.database import get_db
from ....schemas.team import TeamCreate, TeamUpdate, TeamInDB
from ....models.team import Team

router = APIRouter()

@router.get("/", response_model=List[TeamInDB])
def get_teams(
    skip: int = 0,
    limit: int = 100,
    gender: str = None,
    db: Session = Depends(get_db)
):
    """
    Получить список команд с возможностью фильтрации по полу
    """
    query = db.query(Team)
    if gender:
        query = query.filter(Team.gender == gender)
    teams = query.offset(skip).limit(limit).all()
    return teams

@router.post("/", response_model=TeamInDB)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую команду
    """
    db_team = Team(**team.model_dump())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/{team_id}", response_model=TeamInDB)
def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить информацию о конкретной команде по ID
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return team

@router.put("/{team_id}", response_model=TeamInDB)
def update_team(
    team_id: int,
    team: TeamUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить информацию о команде
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    
    for field, value in team.model_dump(exclude_unset=True).items():
        setattr(db_team, field, value)
    
    db.commit()
    db.refresh(db_team)
    return db_team

@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить команду
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    
    db.delete(db_team)
    db.commit()
    return {"message": "Команда успешно удалена"}

@router.get("/{team_id}/stats", response_model=TeamInDB)
def get_team_stats(
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить статистику команды
    """
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    return team

@router.put("/{team_id}/position", response_model=TeamInDB)
def update_team_position(
    team_id: int,
    position: int,
    db: Session = Depends(get_db)
):
    """
    Обновить позицию команды в турнирной таблице
    """
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team is None:
        raise HTTPException(status_code=404, detail="Команда не найдена")
    
    db_team.current_position = position
    db.commit()
    db.refresh(db_team)
    return db_team

@router.get("/standings/{gender}", response_model=List[TeamInDB])
def get_standings(
    gender: str,
    db: Session = Depends(get_db)
):
    """
    Получить турнирную таблицу для указанного пола
    """
    teams = (
        db.query(Team)
        .filter(Team.gender == gender)
        .order_by(Team.current_position)
        .all()
    )
    return teams 