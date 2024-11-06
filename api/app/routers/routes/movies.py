from fastapi import APIRouter
from sqlmodel import select
from app.routers.dependencies import SessionDep
from app.schemas.movie import Movie, Movies


router = APIRouter()


@router.get(
    "/movies",
    tags=["movies"],
    response_model=Movies,
    description="Paginated list of movies",
)
def read_movies(session: SessionDep):
    movies = session.exec(select(Movie)).all()

    return movies
