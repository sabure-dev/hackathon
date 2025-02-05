from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class GenderType(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(Enum(GenderType), nullable=False)
    number = Column(Integer, nullable=False)
    position = Column(String, nullable=False)
    height = Column(Float, nullable=False)  # в сантиметрах
    weight = Column(Float, nullable=False)  # в килограммах
    birth_date = Column(Date, nullable=False)
    biography = Column(String)
    image_url = Column(String)
    
    # Статистика за сезон
    games_played = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    total_rebounds = Column(Integer, default=0)
    total_assists = Column(Integer, default=0)
    total_steals = Column(Integer, default=0)
    total_blocks = Column(Integer, default=0)
    total_turnovers = Column(Integer, default=0)