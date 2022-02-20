from datetime import timedelta

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth import *

app = FastAPI()
auth_service = AuthService()


async def get_auth_user(token: str = Depends(oauth2_scheme)):
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
    except JWTError:
        raise credentials_exception
    user = auth_service.get_user(auth_service.test_db,
                                 username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_active_user(current_user: User = Depends(get_auth_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


@app.post('/token', response_model=Token)
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


@app.get('/users/me/', response_model=User)
async def read_users_me(current_user: User = Depends(get_active_user)):
    return current_user


@app.get('/users/me/items/')
async def read_own_items(current_user: User = Depends(get_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.username}]


if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8000,
        debug=True
    )
