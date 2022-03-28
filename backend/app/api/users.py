from typing import Optional

from app import db, models, schemas
from fastapi import APIRouter, Depends, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import (FilterQuery, SortByDescQuery, SortByQuery,
                   get_active_superuser, get_active_user)

router = APIRouter()


@router.get(path='/me', response_model=schemas.User)
async def user_info(
    user: models.User = Depends(get_active_user)
):
    """Get user info"""

    return user


@router.get(
    path='/{username}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.User)
async def user_get(
    username: str,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.User:
    """Retrieve user with GET request"""

    get_object = await models.User.get(db_session, username=username)
    return get_object


@router.delete(
    path='/{username}',
    status_code=status.HTTP_204_NO_CONTENT)
async def user_delete(
    username: str,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.User:
    """Retrieve user with DELETE request"""

    get_object = await models.User.get(db_session, username=username)
    return await get_object.delete(db_session)


@router.patch(
    path='/{username}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.User)
async def user_patch(
    username: str,
    schema: schemas.UserUpdate,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.User:
    """Modify user with PATCH request"""

    get_object = await models.User.get(db_session, username=username)
    return await get_object.update(db_session, **schema.dict())


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.User])
async def users_list(
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    is_active: Optional[bool] = FilterQuery,
    is_admin: Optional[bool] = FilterQuery,
):
    """List users with GET request"""

    return await models.User.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        is_active=is_active,
        is_admin=is_admin,
    )

add_pagination(router)
