from fastapi.exceptions import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL
engine = None

if config.TESTING:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False})
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
        echo_pool=True,
        pool_size=20,
        max_overflow=20)


Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()


async def get_database():
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
