from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserLogin(UserBase):
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None


class UserCreate(UserUpdate):
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


class User(UserCreate):
    is_admin: Optional[bool] = False
    is_active: Optional[bool] = True

    class Config:
        orm_mode = True


# Additional properties stored in DB
class UserInDB(User):
    hashed_password: str
