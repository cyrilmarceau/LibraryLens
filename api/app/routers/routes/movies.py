from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select, col

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.routers.dependencies import SessionDep
from app.schemas.movie import Movie, MovieQueryParams, MovieUpdate
from app.models.movie import MovieCreate, MoviePublic

router = APIRouter()


@router.post(
    "/movies",
    tags=["movies"],
    description="Get all movies",
    response_description="Return the created movie",
    response_model=MoviePublic,
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
    response_description="List of movies",
    response_model=Page[Movie],
)
async def read_movies(
    *, session: SessionDep, params: Annotated[MovieQueryParams, Query()]
):
    query = select(Movie)

    if params.q:
        query = query.where(Movie.title == params.q)

    order_column = getattr(Movie, params.sort_by, "title")
    order_column = col(order_column)

    if params.order_by == "desc":
        order_column = order_column.desc()

    query = query.order_by(order_column)

    movies = paginate(session, query)

    return movies


@router.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
async def read_movie(*, session: SessionDep, movie_id: int):
    if movie := session.get(Movie, movie_id):
        return movie

    raise HTTPException(status_code=404, detail="Movie not found with ID %s" % movie_id)


@router.put("/movies/{movie_id}", tags=["movies"], response_model=Movie)
async def update_movie(*, session: SessionDep, movie_id: int, movie: MovieUpdate):
    if db_movie := session.get(Movie, movie_id):
        movie_data = movie.model_dump(exclude_unset=True)
        db_movie.sqlmodel_update(movie_data)

        session.add(db_movie)
        session.commit()
        session.refresh(db_movie)

        return db_movie

    raise HTTPException(status_code=404, detail="Movie not found with ID %s" % movie_id)
