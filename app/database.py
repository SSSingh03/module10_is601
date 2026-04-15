import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/postgres"
    )


settings = Settings()

Base = declarative_base()


def get_engine(database_url: str | None = None):
    url = database_url or settings.DATABASE_URL
    return create_engine(url)


def get_sessionmaker(engine=None):
    if engine is None:
        engine = get_engine()
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )


engine = get_engine()
SessionLocal = get_sessionmaker(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()