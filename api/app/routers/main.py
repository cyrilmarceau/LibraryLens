from fastapi import APIRouter
from app.routers.routes import movies, books, tv_shows

api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(movies.router)
api_router.include_router(books.router)
api_router.include_router(tv_shows.router)
