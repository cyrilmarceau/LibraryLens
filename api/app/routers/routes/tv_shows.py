from fastapi import APIRouter

router = APIRouter()


@router.get("/tv_shows", tags=["tv_shows"])
async def read_tv_shows():
    return [{"name": "The Crown"}, {"name": "The Mandalorian"}]
