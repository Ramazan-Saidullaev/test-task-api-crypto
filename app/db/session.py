from functools import lru_cache

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


@lru_cache
def get_engine():
    settings = get_settings()
    return create_engine(settings.database_url, future=True)


@lru_cache
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, class_=Session)


def get_db():
    db = get_session_factory()()
    try:
        yield db
    finally:
        db.close()


def ensure_database_schema() -> None:
    engine = get_engine()

    with engine.begin() as connection:
        inspector = inspect(connection)

        if not inspector.has_table("price_records"):
            return

        columns = {column["name"] for column in inspector.get_columns("price_records")}

        if "timestamp_unix" not in columns and "timestamp" in columns:
            connection.execute(
                text("ALTER TABLE price_records RENAME COLUMN timestamp TO timestamp_unix")
            )
