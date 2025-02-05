from fastapi import APIRouter
from .endpoints import players, news, games, teams

api_router = APIRouter()

api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(games.router, prefix="/games", tags=["games"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"]) 