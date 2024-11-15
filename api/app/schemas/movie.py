from datetime import datetime, timezone

from sqlmodel import Field, SQLModel
from .media import MediaPlatform, MediaType


class MovieBase(SQLModel):
    title: str
    is_liked: bool = False
    is_watched: bool = False
    media_type: MediaType = Field(
        default=MediaType.MOVIE, description="Type of media (read-only)"
    )
    media_platform: MediaPlatform | None = Field(
        default=None, description="Platform where the movie is available"
    )

    class Config:
        orm_mode = True
        use_enum_values = True


class Movie(MovieBase, table=True):
    id: int = Field(default=None, primary_key=True, description="ID of the movie")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Creation time of the movie (read-only)",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": datetime.now(timezone.utc)},
        description="Last updated time of the movie (read-only)",
    )