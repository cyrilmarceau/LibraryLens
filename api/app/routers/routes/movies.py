from typing import Annotated

from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select, col
from app.routers.dependencies import SessionDep
from app.schemas.movie import Movie, MovieQueryParams
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
    response_model=list[Movie],
)
async def read_movies(
    *,
    session: SessionDep,
    params: Annotated[MovieQueryParams, Query()]
):
    query = select(Movie)

    if params.q:
        query = query.where(Movie.title == params.q)


    order_column = getattr(Movie, params.sort_by, "title")
    order_column = col(order_column)

    if params.order_by == "desc":
        order_column = order_column.desc()

    query = query.order_by(order_column).offset(params.offset).limit(params.limit)

    # Execute the query
    movies = session.exec(query).all()

    return movies


@router.get("/movies/{movie_id}", tags=["movies"], response_model=Movie)
async def read_movie(*, session: SessionDep, movie_id: int):
    if movie := session.get(Movie, movie_id):
        return movie

    raise HTTPException(status_code=404, detail="Movie not found with ID %s" % movie_id)
