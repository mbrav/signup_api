from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .deps import get_active_user

router = APIRouter()


@router.get(path='/me', response_model=schemas.User)
async def user_info(
    user: models.User = Depends(get_active_user)
):
    """Get user info"""

    return user


@router.get(path='/me/signups')
async def user_items(
    user: models.User = Depends(get_active_user)
):
    """Get user's signups"""

    return [{'signup_id': 'Foo', 'owner': user.username}]
