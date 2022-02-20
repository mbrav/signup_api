from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..db import Base


class User(Base):
    """User class"""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), nullable=False)
    hashed_password = Column(Text(), nullable=False)
    email = Column(String(30), nullable=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    # signups = relationship('User', back_populates='owner')

    def __init__(self,
                 username: str,
                 password: str,
                 email: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 is_active: bool = True,
                 is_superuser: bool = False):
        self.username = username
        self.hashed_password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_superuser = is_superuser
