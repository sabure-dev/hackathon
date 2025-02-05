from sqlalchemy import Column, Integer, String, Enum, Float
from sqlalchemy.orm import relationship
from ..core.database import Base
from .player import GenderType

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    logo_url = Column(String)
    
    # Турнирная статистика
    games_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    points_scored = Column(Integer, default=0)
    points_conceded = Column(Integer, default=0)
    current_position = Column(Integer)  # место в турнирной таблице
    
    # Вычисляемые поля
    win_percentage = Column(Float, default=0.0)
    points_difference = Column(Integer, default=0) 