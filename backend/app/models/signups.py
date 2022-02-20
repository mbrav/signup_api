from app.db import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Signup(Base):
    """Signup class"""

    __tablename__ = 'signups'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String(30), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    class_id = Column(String(60), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    # user = relationship('User', back_populates='signups')

    def __init__(self,
                 first_name: str,
                 last_name: str,
                 phone: str,
                 email: str,
                 class_id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.class_id = class_id
