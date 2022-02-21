from datetime import timedelta

from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .deps import auth_service, get_active_user

router = APIRouter()


@router.post(auth_service.TOKEN_URL,
             response_model=schemas.Token,
             tags=['auth'])
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(db.get_database)):
    user = await auth_service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=auth_service.TOKEN_EXPIRE_MINUTES)
    data = {'sub': user.username}
    access_token = auth_service.create_access_token(
        data=data, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/users/register',
             response_model=schemas.UserBase,
             status_code=status.HTTP_201_CREATED,
             tags=['auth'])
async def read_users_register(
        schema: schemas.UserCreate,
        db: Session = Depends(db.get_database)):
    async def create():
        user = db.query(
            models.User).filter(
            models.User.username == schema.username).first()
        if user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Username '{schema.username}' already taken",
                headers={'WWW-Authenticate': 'Bearer'})
        hashed_password = auth_service.hash_password(schema.password)
        new_object = models.User(
            username=schema.username,
            password=hashed_password)
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        return new_object
    return await create()


@router.get('/users/me', response_model=schemas.User, tags=['auth'])
async def read_users_me(user: models.User = Depends(get_active_user)):
    return user


@router.get('/users/me/signups', tags=['auth'])
async def read_own_items(user: models.User = Depends(get_active_user)):
    return [{'item_id': 'Foo', 'owner': user.username}]
