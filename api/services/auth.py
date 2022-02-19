from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class AuthService:
    """"Auth Servie Class"""

    def __init__(
            self,
            secret: str = 'p!E@Zech@ngeme!',
            algorithm: str = 'HS256',
            expire: int = 30,
            token_url: str = 'token'):
        """Auth service initialization"""
        self.SECRET_KEY = secret
        self.CRYPT_ALGORITHM = algorithm
        self.TOKEN_EXPIRE_MINUTES = expire

        self.context = context
        self.oauth2_scheme = oauth2_scheme

        self.test_db = {
            'user': {
                'username': 'user',
                'full_name': 'John Doe',
                'email': 'user@example.com',
                'hashed_password': self.get_password_hash('user'),
                'disabled': False,
            }
        }

    def verify_password(self, plain_password, hashed_password):
        return context.verify(plain_password, hashed_password)

    def authenticate_user(self, db, username: str, password: str):
        user = self.get_user(db, username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self,
                            data: dict,
                            expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            delta = timedelta(minutes=self.TOKEN_EXPIRE_MINUTES)
            expire = datetime.utcnow() + delta
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode,
                                 self.SECRET_KEY,
                                 algorithm=self.CRYPT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_user(db, username: str):
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)

    @staticmethod
    def get_password_hash(password):
        return context.hash(password)
