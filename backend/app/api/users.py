from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .deps import auth_service, get_active_user

router = APIRouter()


@router.post(path='/register',
             response_model=schemas.UserBase,
             status_code=status.HTTP_201_CREATED)
async def user_register(
        schema: schemas.UserCreate,
        db: Session = Depends(db.get_database)) -> models.User:
    async def create() -> models.User:
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


@router.get(path='/me', response_model=schemas.User)
async def user_info(user: models.User = Depends(get_active_user)):
    return user


@router.get(path='/me/signups')
async def user_items(user: models.User = Depends(get_active_user)):
    return [{'signup_id': 'Foo', 'owner': user.username}]
