from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..services.auth import Token, User  # remove me
from . import schemas
from .deps import auth_service, get_active_user

router = APIRouter()


@router.post('/token', response_model=Token, tags=['auth'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(auth_service.test_db,
                                          form_data.username,
                                          form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=auth_service.TOKEN_EXPIRE_MINUTES)
    data = {'sub': user.username}
    access_token = auth_service.create_access_token(
        data=data, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/me', response_model=User, tags=['auth'])
async def read_users_me(user: User = Depends(get_active_user)):
    return user


@router.get('/users/me/signups', tags=['auth'])
async def read_own_items(user: User = Depends(get_active_user)):
    return [{'item_id': 'Foo', 'owner': user.username}]
