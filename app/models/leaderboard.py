from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..core.database import Base
import enum

class Leaderboard(Base):
    __tablename__ = "leaderboard"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    games = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    scored = Column(Integer, nullable=False)
    conceded = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False)
