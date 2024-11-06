from enum import Enum

from sqlmodel import Field, SQLModel


class MediaType(str, Enum):
    BOOK = "book"
    TV_SHOW = "tv_show"
    MOVIE = "movie"


class Media(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(default=None)
