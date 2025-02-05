from pydantic import BaseModel

class LeaderboardBase(BaseModel):
    name: str = ''
    games: int = 0
    wins: int = 0
    losses: int = 0
    scored: int = 0
    conceded: int = 0
    position: int = 0

class LeaderboardCreate(LeaderboardBase):
    pass

class LeaderboardUpdate(BaseModel):
    name: str | None = None
    games: int | None = None
    wins: int | None = None
    losses: int | None = None
    scored: int | None = None
    conceded: int | None = None
    position: int | None = None

class LeaderboardInDB(LeaderboardBase):
    id: int
