from datetime import datetime, timedelta
from typing import Optional, Union

from sqlalchemy import Boolean, Column, ForeignKey, Integer, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, relationship

from .base import BaseModel
from .events import Event
from .users import User


class Signup(BaseModel):
    """Signup class"""

    cancelled = Column(Boolean(), default=False)
    notification = Column(Boolean(), default=True)

    event_id = Column(Integer, ForeignKey(Event.id))
    event = relationship('Event', back_populates='signups')

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='signups')

    def __init__(self,
                 user_id: int,
                 event_id: int,
                 cancelled: bool = False,
                 notification: bool = True):
        self.user_id = user_id
        self.event_id = event_id
        self.cancelled = cancelled
        self.notification = notification

    @classmethod
    async def by_user(
        self,
        db_session: AsyncSession,
        user_id: int,
        hours_ago: Optional[Union[int, None]] = 0,
        limit: int = None,
        offset: int = 0
    ):
        """Get signups of a user newer than hours_ago

        Args:
            db_session (AsyncSession): Current db session
            user_id (int): User id
            hours_ago (Union[int, None], optuser_idional): Ignore events before n hours ago.
            Show all events if None. Defaults to 0.
            limit (int, optional): limit result. Defaults to None.
            offset (int, optional): offset result. Defaults to 0.

        Returns:
            query result 
        """

        db_query = select(self).join(
            self.event).options(
            joinedload(self.event)).filter(
            self.user_id == user_id)

        if hours_ago is not None:
            db_query = db_query.where(
                Event.start > datetime.utcnow() -
                timedelta(hours=hours_ago))

        if limit:
            db_query = db_query.limit(limit).offset(offset)

        return await self.get_list(db_session, db_query=db_query)
