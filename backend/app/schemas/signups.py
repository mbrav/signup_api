from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupIn(BaseModel):
    first_name: Optional[str] = Field(example='Linus')
    last_name: Optional[str] = Field(example='Trovalds')
    phone: Optional[str] = Field(example='+12001234545')
    email: Optional[EmailStr] = Field(example='linus@linux.org')

    user_id: Optional[int] = Field(example=1)
    event_id: int = Field(example=1)

    class Config:
        orm_mode = True


class SignupOut(SignupIn):
    created_at: datetime
    id: int = Field(example=1)
