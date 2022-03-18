from datetime import timedelta

from app import db, models, schemas
from app.services import AuthService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import auth_service, get_active_user

router = APIRouter()


@router.post(path='/token', response_model=schemas.Token)
async def access_token_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db_session: AsyncSession = Depends(db.get_database)
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
    access_token = await auth_service.create_access_token(
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
    schema: schemas.UserLogin,
    db_session: AsyncSession = Depends(db.get_database)
) -> models.User:
    """Register new user"""

    model = models.User

    stmt = select(model).where(model.username == schema.username)
    result = await db_session.execute(stmt)
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Username '{schema.username}' already taken",
            headers={'WWW-Authenticate': 'Bearer'})

    hashed_password = auth_service.hash_password(schema.password)
    new_object = model(
        username=schema.username,
        password=hashed_password)

    db_session.add(new_object)
    await db_session.commit()
    return new_object
