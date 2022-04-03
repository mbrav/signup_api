from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserLogin(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class UserCreate(UserUpdate):
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True


class UserCreateTg(UserBase):
    is_active: bool = False
    first_name: Optional[str] = ''
    last_name: Optional[str] = ''
    tg_id: int


class User(UserCreate):
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True
