from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from .events import Event
from .users import User


class Signup(BaseModel):
    """Signup class"""

    event_id = Column(Integer, ForeignKey(Event.id))
    event = relationship('Event', back_populates='signups')

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='signups')

    def __init__(self,
                 user_id: int,
                 event_id: int):
        self.user_id = user_id
        self.event_id = event_id
