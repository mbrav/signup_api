# from app.models.user import UserPasswordUpdate
from passlib.context import CryptContext
from passlib.hash import argon2

# from ..models.user import UserPasswordUpdate

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


class AuthException(BaseException):
    """ Custom auth exception that can be modified later on."""
    pass


class AuthService:
    def create_salt_and_hashed_password(
            self, *, plaintext_password: str) -> UserPasswordUpdate:
        hashed_password = self.hash_password(
            password=plaintext_password, salt=salt)
        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return argon2.hash('sdfasdfasdf')

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)
