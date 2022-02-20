from datetime import datetime, timedelta
from typing import Optional

from app import db, models, schemas
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

context = CryptContext(schemes=['argon2'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class AuthService:
    """"Auth Service Class"""

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
        self.TOKEN_URL = token_url

        self.context = context
        self.oauth2_scheme = oauth2_scheme

    @staticmethod
    def get_user(username: str,
                 db: Session = Depends(db.get_database)) -> models.User:
        """Get user from database"""
        user = db.query(
            models.User).filter(
            models.User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=404, detail=f'User "{username}" not registered')
        return user

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(password) -> str:
        return context.hash(password)

    def authenticate_user(
            self, username: str, password: str,
            db: Session = Depends(db.get_database)) -> models.User:
        """Authenticate user"""
        user = self.get_user(username=username, db=db)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self,
                            data: dict,
                            expires_delta: Optional[timedelta] = None):
        """Encode Token"""
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
