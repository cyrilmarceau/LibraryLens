from datetime import datetime, timezone

from sqlmodel import Field
from sqlmodel import SQLModel
from .media import Media, MediaType, MediaPlatform


class Movie(Media, table=True):
    id: int = Field(default=None, primary_key=True, description="ID of the movie")
    is_liked: bool = Field(default=False, description="Is the movie liked by the user")
    is_watched: bool = Field(
        default=False, description="Has the user watched the movie"
    )
    media_type: MediaType = Field(
        default=MediaType.MOVIE, description="Type of media (read-only)"
    )
    media_platform: MediaPlatform = Field(
        default=None, description="Platform where the movie is available"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation time of the movie (read-only)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        description="Last updated time of the movie (read-only)",
    )


class Movies(SQLModel):
    data: list[Movie]
    count: int
