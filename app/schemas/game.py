from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .player import GenderType

class GameBase(BaseModel):
    gender: GenderType
    team_name: str
    date_time: datetime
    location: str
    is_home_game: bool
    score_black_bears: Optional[int] = None
    score_opponent: Optional[int] = None

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    gender: Optional[GenderType] = None
    team_name: Optional[str] = None
    date_time: Optional[datetime] = None
    location: Optional[str] = None
    is_home_game: Optional[bool] = None
    score_black_bears: Optional[int] = None
    score_opponent: Optional[int] = None

class GameInDB(GameBase):
    id: int

    class Config:
        from_attributes = True
