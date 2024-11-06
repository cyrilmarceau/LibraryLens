from fastapi import FastAPI

from sqlmodel import SQLModel

from .core.config import settings
from .routers.main import api_router
from app.core.db import engine


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI(
    title=settings.app_name,
    redirect_slashes=False,
    version=settings.app_version,
)

app.include_router(api_router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
