from typing import AsyncGenerator

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

engine = None

if settings.TESTING:
    # Create sqlite database if testing
    engine = create_async_engine(
        settings.SQLITE_DATABASE_FILE,
        future=True,
        echo=settings.DEBUG,
        connect_args={'check_same_thread': False}
    )
else:
    engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        echo_pool=True,
        pool_size=20,
        max_overflow=20
    )


Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()


# Dependency
async def get_database() -> AsyncGenerator:
    async with Session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            session.rollback()
            raise http_ex
        finally:
            await session.close()
