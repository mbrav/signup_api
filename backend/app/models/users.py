from sqlalchemy import BigInteger, Boolean, Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    """User class"""

    username = Column(String(16), nullable=False)
    hashed_password = Column(String(128), nullable=True)

    tg_id = Column(BigInteger, nullable=True)
    email = Column(String(32), nullable=True)
    first_name = Column(String(32), nullable=True)
    last_name = Column(String(32), nullable=True)
    is_active = Column(Boolean(), default=True)
    is_admin = Column(Boolean(), default=False)

    # IETF language tag
    # https://en.wikipedia.org/wiki/IETF_language_tag
    language_code = Column(String(8), default='en')

    signups = relationship('Signup', back_populates='user')
    tasks = relationship('Task', back_populates='user')

    def __init__(self,
                 username: str,
                 password: str = None,
                 tg_id: int = None,
                 email: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 language_code: str = None,
                 is_active: bool = True,
                 is_admin: bool = False):

        self.username = username
        self.hashed_password = password
        self.tg_id = tg_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.language_code = language_code
        self.is_active = is_active
        self.is_admin = is_admin
