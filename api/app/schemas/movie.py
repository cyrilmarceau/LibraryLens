from sqlmodel import Field
from sqlmodel import SQLModel
from .media import Media, MediaType


class Movie(Media, table=True):
    id: int = Field(default=None, primary_key=True)
    is_liked: bool = Field(default=False, description="Is the movie liked by the user")
    is_watched: bool = Field(
        default=False, description="Has the user watched the movie"
    )
    media_type: MediaType = Field(
        default=MediaType.MOVIE, description="Type of media (read-only)"
    )


class Movies(SQLModel):
    data: list[Movie]
    count: int
