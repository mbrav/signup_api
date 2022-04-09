from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SignupIn(BaseModel):
    user_id: int = Field(example=1)
    event_id: int = Field(example=1)

    class Config:
        orm_mode = True


class SignupOut(SignupIn):
    created_at: datetime
    updated_at: Optional[datetime]
    id: int = Field(example=1)
