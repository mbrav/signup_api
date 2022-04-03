from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from .base import BaseModel


class Event(BaseModel):
    """Event class"""

    name = Column(String(100), nullable=False)
    description = Column(Text, default='')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)

    google_modified = Column(DateTime, nullable=True)
    google_id = Column(String(30), nullable=True)

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
    async def get_current(self, db_session: AsyncSession, days_ago: int = 1):
        """Get events newer than days_ago"""

        db_query = select(self).where(
            self.start > datetime.utcnow() - timedelta(days=days_ago)
        ).order_by(
            self.start.asc())

        return await self.get_list(db_session, db_query=db_query)
