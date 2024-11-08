from enum import Enum

from sqlmodel import Field, SQLModel


class MediaType(str, Enum):
    BOOK = "book"
    TV_SHOW = "tv_show"
    MOVIE = "movie"


class MediaPlatform(str, Enum):
    NETFLIX = "netflix"
    PRIME = "prime"
    DISNEY = "disney"
    CANAL = "canal"


class Media(SQLModel):
    id: int = Field(default=None, primary_key=True, description="ID of the media")
    title: str = Field(default=None, description="Title of the media")
