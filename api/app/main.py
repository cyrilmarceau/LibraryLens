import logging

from typing import Union, Annotated

from fastapi import FastAPI, Depends

from sqlmodel import create_engine, Session, SQLModel

from .routers import books, tv_shows, movies
from .config import settings


engine = create_engine(
    f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}",
    echo=True,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_sessions():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_sessions)]

app = FastAPI(
    title=settings.app_name,
    redirect_slashes=False,
)

app.include_router(books.router)
app.include_router(tv_shows.router)
app.include_router(movies.router)


@app.on_event("startup")
def on_startup():
    logger = logging.getLogger("uvicorn.info")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    create_db_and_tables()


@app.get("/")
def read_root():
    return {"Hello": "Library Lens API"}
