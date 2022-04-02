from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from .events import Event
from .users import User


class Signup(BaseModel):
    """Signup class"""

    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String(30), nullable=False)

    event_id = Column(Integer, ForeignKey(Event.id))
    event = relationship('Event', back_populates='signups')

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship('User', back_populates='signups')

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 phone: str,
                 email: str,
                 user_id: int,
                 event_id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.event_id = event_id
