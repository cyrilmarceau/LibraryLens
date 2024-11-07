from typing import Annotated

from fastapi import APIRouter, Query
from sqlmodel import select
from app.routers.dependencies import SessionDep
from app.schemas.movie import Movie, Movies

router = APIRouter()


@router.get(
    "/movies",
    tags=["movies"],
    description="Get all movies",
    response_description="List of movies"
)
def read_movies(
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
) -> Movies:
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()

    return Movies(data=movies, count=len(movies))


@router.post(
    "/movies",
    tags=["movies"],
    response_model=Movie,
    description="Create a new movie",
)
def create_movie(movie: Movie, session: SessionDep) -> Movie:
    session.add(movie)
    session.commit()
    session.refresh(movie)

    return movie
