from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class GenderType(str, Enum):
    MALE = "male"
    FEMALE = "female"

class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    gender: GenderType
    number: int
    position: str
    height: float
    weight: float
    birth_date: date
    biography: Optional[str] = None
    image_url: Optional[str] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[GenderType] = None
    number: Optional[int] = None
    position: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    birth_date: Optional[date] = None

class PlayerInDB(PlayerBase):
    id: int
    games_played: int = 0
    total_points: int = 0
    total_rebounds: int = 0
    total_assists: int = 0
    total_steals: int = 0
    total_blocks: int = 0
    total_turnovers: int = 0

    class Config:
        from_attributes = True 