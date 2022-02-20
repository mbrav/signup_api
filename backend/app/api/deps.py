from app import config
from app.services import AuthService
from app.services.auth import Token, TokenData, User  # remove me
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError

auth_service = AuthService(secret=config.SECRET_KEY,
                           algorithm=config.CRYPT_ALGORITHM,
                           expire=config.TOKEN_EXPIRE_MINUTES)


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
