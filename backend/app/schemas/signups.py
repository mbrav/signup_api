from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class SignupCreate(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[EmailStr] = None
    class_id: Optional[str] = None

    class Config:
        orm_mode = True


class SignupOut(SignupCreate):
    created_at: datetime
    user_id: Optional[int] = None
    id: int
