# src/spendtrackr/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from spendtrackr.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.sqlalchemy_database_uri,
    echo=settings.debug,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Session:
    """
    FastAPI dependency that yields a DB session and closes it after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
