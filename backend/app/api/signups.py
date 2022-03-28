from typing import Optional

from app import db, models, schemas
from fastapi import APIRouter, Depends, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import (FilterQuery, SortByDescQuery, SortByQuery,
                   get_active_superuser, get_active_user)

router = APIRouter()


@router.post(
    path='',
    response_model=schemas.SignupOut,
    status_code=status.HTTP_201_CREATED)
async def signup_post(
    schema: schemas.SignupIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database)
) -> models.Signup:
    """Create new signup with POST request"""

    new_object = models.Signup(**schema.dict())
    return await new_object.save(db_session)


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SignupOut)
async def signup_get(
    id: int,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Signup:
    """Retrieve signup with GET request"""

    get_object = await models.Signup.get(db_session, id=id)
    return get_object


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def signup_delete(
    id: int,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Signup:
    """Retrieve signup with GET request"""

    get_object = await models.Signup.get(db_session, id=id)
    return await get_object.delete(db_session)


@router.patch(
    path='/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.SignupOut)
async def signup_patch(
    id: int,
    schema: schemas.SignupIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Signup:
    """Modify signup with PATCH request"""

    get_object = await models.Signup.get(db_session, id=id)
    return await get_object.update(db_session, **schema.dict())


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.SignupOut])
async def signups_list(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    first_name: Optional[str] = FilterQuery,
    last_name: Optional[str] = FilterQuery,
    phone: Optional[str] = FilterQuery,
    email: Optional[str] = FilterQuery,
    class_id: Optional[str] = FilterQuery,
    user_id: Optional[int] = FilterQuery
):
    """List signups with GET request"""

    return await models.Signup.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        class_id=class_id,
        user_id=user_id,
    )

add_pagination(router)
