from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base
from .player import GenderType


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(Enum(GenderType), nullable=False)
    team_name = Column(String, ForeignKey("teams.name", onupdate="CASCADE"), nullable=False)
    date_time = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    is_home_game = Column(Boolean, nullable=False)
    score_black_bears = Column(Integer)
    score_opponent = Column(Integer)
    
    # Связь с командой
    team = relationship("Team", back_populates="games")
    