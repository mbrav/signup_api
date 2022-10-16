from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, String, Text, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from .base import BaseModel


class Event(BaseModel):
    """Event class"""

    name = Column(String(128), nullable=False)
    description = Column(Text, default='')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)

    google_modified = Column(DateTime, nullable=True)
    google_id = Column(String(128), nullable=True)

    signups = relationship('Signup', back_populates='event')

    def __init__(self,
                 name: str,
                 start: datetime,
                 description: str = '',
                 end: datetime = None,
                 google_modified: datetime = None,
                 google_id: str = None
                 ):
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.google_modified = google_modified
        self.google_id = google_id

    @classmethod
    async def get_current(
        self,
        db_session: AsyncSession,
        hours_ago: int = 0,
        limit: int = None,
        offset: int = 0
    ):
        """Get events newer than hours_ago

        Args:
            db_session (AsyncSession): Current db session
            hours_ago (int, optional): Ignore events before n hours ago.
            Defaults to 0.
            limit (int, optional): limit result. Defaults to 0.
            offset (int, optional): offset result. Defaults to 0.

        Returns:
            query result 
        """

        db_query = select(self).where(
            self.start > datetime.utcnow() - timedelta(hours=hours_ago)
        ).order_by(
            self.start.asc())

        if limit:
            db_query = db_query.limit(limit).offset(offset)

        return await self.get_list(db_session, db_query=db_query)

    @classmethod
    async def get_current_count(
        self,
        db_session: AsyncSession,
        hours_ago: int = 0,
    ) -> int:
        """Return count only of events newer than hours_ago"""

        db_query = select([func.count()]).select_from(self).where(
            self.start > datetime.utcnow() - timedelta(hours=hours_ago))
        result = await db_session.execute(db_query)
        return result.scalar()
