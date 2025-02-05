from pydantic import BaseModel
from typing import Optional, List
from .player import GenderType

class TeamBase(BaseModel):
    name: str
    gender: GenderType
    logo_url: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    name: Optional[str] = None
    gender: Optional[GenderType] = None
    logo_url: Optional[str] = None
    games_played: Optional[int] = None
    wins: Optional[int] = None
    losses: Optional[int] = None
    points_scored: Optional[int] = None
    points_conceded: Optional[int] = None
    current_position: Optional[int] = None

class TeamInDB(TeamBase):
    id: int
    games_played: int = 0
    wins: int = 0
    losses: int = 0
    points_scored: int = 0
    points_conceded: int = 0
    current_position: Optional[int] = None
    win_percentage: float = 0.0
    points_difference: int = 0

    class Config:
        from_attributes = True