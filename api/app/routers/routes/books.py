from fastapi import APIRouter

router = APIRouter()


@router.get("/books", tags=["books"])
async def read_books():
    return [{"name": "The Great Gatsby"}, {"name": "To Kill a Mockingbird"}]
