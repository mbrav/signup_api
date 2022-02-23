from datetime import timedelta

from app import db, models, schemas
from app.services import AuthService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .deps import auth_service, get_active_user

router = APIRouter()


@router.post(path='/token', response_model=schemas.Token)
async def access_token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: Session = Depends(db.get_database)
) -> schemas.Token:
    """Get token based on provided OAuth2 credentials"""

    user = await auth_service.authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db_session=db_session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=auth_service.TOKEN_EXPIRE_MINUTES)
    data = {'sub': user.username}
    access_token = auth_service.create_access_token(
        data=data,
        expires_delta=access_token_expires)

    response = schemas.Token(
        access_token=access_token,
        token_type='bearer')
    return response


@router.post(
    path='/register',
    response_model=schemas.UserBase,
    status_code=status.HTTP_201_CREATED)
async def user_register(
    schema: schemas.UserCreate,
    db_session: Session = Depends(db.get_database)
) -> models.User:
    """Register new user"""

    async def create() -> models.User:
        user = db_session.query(
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
        db_session.add(new_object)
        db_session.commit()
        db_session.refresh(new_object)
        return new_object
    return await create()
