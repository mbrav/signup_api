from fastapi import HTTPException, status
from sqlalchemy import Column, DateTime, Integer, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.sql import func

Base = declarative_base()


def to_snake_case(str: str) -> str:
    res = [str[0].lower()]
    for c in str[1:]:
        if c in ('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            res.append('_')
            res.append(c.lower())
        else:
            res.append(c)
    return ''.join(res)


class BaseModel(Base):
    """Abstract base model"""

    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def __tablename__(self) -> str:
        return to_snake_case(self.__name__) + 's'

    async def save(self, db_session: AsyncSession):
        """Save object
        Save method is not a @classmethod since we need an instantiated object 

        Args:
            db_session (AsyncSession): Current db session

        Raises:
            HTTPException: Raise SQLAlchemy error
        """
        try:
            db_session.add(self)
            await db_session.commit()
            await db_session.refresh(self)
            return self
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    @classmethod
    async def get(
        self,
        db_session: AsyncSession,
        query: select = None,
        **kwarg
    ):
        """Get object based on query or id identified by kwarg
        If no query or id is passed, value is returned based on whether
        any tables exist in the table or not.

        Args:
            db_session (AsyncSession): Current db session
            query (select, optional): Query. Defaults to None.
            kwarg (optional): Object attribute and value by which
                to get object. Defaults to None.

        Raises:
            HTTPException: Raise SQLAlchemy error

        Returns:
            Query result
        """

        if query is None:
            if not len(kwarg):
                query = select(self)
            else:
                key, value = kwarg.popitem()
                query = select(self).where(getattr(self, key) == value)

        try:
            result = await db_session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))

    @classmethod
    async def update(self, db_session: AsyncSession, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.save(db_session)

    @classmethod
    async def delete(self, db_session: AsyncSession):
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex))
