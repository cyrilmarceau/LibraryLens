from sqlmodel import create_engine
from app.core.config import settings


engine = create_engine(
    f"mysql+pymysql://{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}",
    echo=True,
)
