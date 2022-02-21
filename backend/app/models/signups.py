from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class Signup(BaseModel):
    """Signup class"""

    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone = Column(String(12), nullable=False)
    email = Column(String(30), nullable=False)

    class_id = Column(String(60), nullable=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    # user = relationship('User', back_populates='signup')

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
