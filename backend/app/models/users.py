from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """User class"""

    username = Column(String(20), nullable=False)
    hashed_password = Column(String(130), nullable=False)
    email = Column(String(30), nullable=True)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)

    # signups = relationship('User', back_populates='owner')

    def __init__(self,
                 username: str,
                 password: str = None,
                 email: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 is_active: bool = True,
                 is_admin: bool = False):
        self.username = username
        self.hashed_password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_admin = is_admin
