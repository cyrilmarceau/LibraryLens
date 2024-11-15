from datetime import datetime

from app.schemas.movie import MovieBase


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    pass


class MoviePublic(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime
