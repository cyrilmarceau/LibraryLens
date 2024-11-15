from enum import Enum


class MediaType(str, Enum):
    BOOK = "book"
    TV_SHOW = "tv_show"
    MOVIE = "movie"


class MediaPlatform(str, Enum):
    NETFLIX = "netflix"
    PRIME = "prime"
    DISNEY = "disney"
    CANAL = "canal"
