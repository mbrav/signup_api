from app import config
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError

from ..services.auth import Token, TokenData, User  # remove me
from . import AuthService, db, models, schemas

auth_service = AuthService(secret=config.SECRET_KEY,
                           algorithm=config.CRYPT_ALGORITHM,
                           expire=config.TOKEN_EXPIRE_MINUTES)


def create_superuser(username: str,
                     password: str,
                     session=db.get_db,
                     schema=schemas.UserCreate) -> None:
    """
    Tables should be created with Alembic migrations
    But if you don't want to use migrations, create
    the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)
    """
    db = session()
    user = db.query(models.User).count() != 0
    if not user:
        hashed_password = auth_service.get_password_hash(password)
        user_in = schema(
            username=username,
            password=hashed_password,
            is_superuser=True)
        new_user = models.User(**user_in.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)


async def get_auth_user(
        token: str = Depends(auth_service.oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, auth_service.SECRET_KEY,
                             algorithms=[auth_service.CRYPT_ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = auth_service.get_user(auth_service.test_db,
                                 username=token_data.username)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


async def get_active_user(
        current_user: User = Depends(get_auth_user)) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


def get_active_superuser(
    current_user: User = Depends(get_auth_user),
) -> User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
