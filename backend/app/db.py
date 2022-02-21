from typing import Generator

from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

DATABASE_URL = settings.DATABASE_URL
engine = None

if settings.TESTING:
    engine = create_engine(
        DATABASE_URL,
        connect_args={'check_same_thread': False})
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo_pool=True,
        pool_size=20,
        max_overflow=20)


Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()


def get_db():
    db = Session()
    return db


async def get_database() -> Generator:
    """Fresh implementation of 0.74 feature
    https://github.com/tiangolo/fastapi/releases/tag/0.74.0
    """
    with Session() as session:
        try:
            yield session
        except HTTPException:
            session.rollback()
            raise
        finally:
            session.close()
