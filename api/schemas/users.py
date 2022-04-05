from datetime import datetime

from pydantic import BaseModel


class UserIn(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True


class UserOut(UserIn):
    created_at: datetime
    id: int
