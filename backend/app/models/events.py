from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Event(BaseModel):
    """Event class"""

    name = Column(String(100), nullable=False)
    description = Column(Text, default='')
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)

    google_id = Column(String(30), nullable=True)

    signups = relationship('Signup', back_populates='event')

    def __init__(self,
                 name: str,
                 start: datetime,
                 description: str = '',
                 end: datetime = None,
                 google_id: str = None
                 ):
        self.name = name
        self.description = description
        self.start = start
        self.end = end
        self.google_id = google_id
