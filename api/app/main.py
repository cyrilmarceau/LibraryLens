import logfire

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

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

logfire.configure()
logfire.instrument_fastapi(app)

app.include_router(api_router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
