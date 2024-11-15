from typing import Annotated

from fastapi import APIRouter, Query, HTTPException, Form
from sqlmodel import select
from app.routers.dependencies import SessionDep
from app.schemas.movie import Movie
from app.models.movie import MovieCreate, MoviePublic

router = APIRouter()


@router.post(
    "/movies",
    tags=["movies"],
    description="Get all movies",
    response_description="Return the created movie",
    response_model=MoviePublic
)
async def create_movie(*, session: SessionDep, movie: MovieCreate):
    new_movie = Movie.model_validate(movie)
    session.add(new_movie)
    session.commit()
    session.refresh(new_movie)

    return new_movie


@router.get(
    "/movies",
    tags=["movies"],
    description="Get all movies",
    response_description="List of movies"
)
async def read_movies(
        *,
        session: SessionDep,
        offset: int = 0,
        limit: Annotated[int, Query(le=100)] = 100
):
    movies = session.exec(select(Movie).offset(offset).limit(limit)).all()

    return movies


@router.get('/movies/{movie_id}', tags=["movies"], response_model=Movie)
async def read_movie(*,  session: SessionDep, movie_id: int):
    if movie := session.get(Movie, movie_id):
        return movie

    raise HTTPException(status_code=404, detail="Movie not found with ID %s" % movie_id)
