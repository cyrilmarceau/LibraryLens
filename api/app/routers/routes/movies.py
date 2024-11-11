from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
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
async def read_movies(
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
def create_movie(movie: Movie, session: SessionDep):

    print(movie.model_dump_json(indent=4))

    if session.get(Movie, movie.id):
        raise HTTPException(status_code=400, detail="Movie already exists")

    movie

    session.add(movie)
    session.commit()
    session.refresh(movie)

    return movie


@router.get('/movies/{movie_id}', tags=["movies"], response_model=Movie)
async def read_movie(movie_id: int, session: SessionDep):
    if movie := session.get(Movie, movie_id):
        return movie

    raise HTTPException(status_code=404, detail="Movie not found with ID %s" % movie_id)
