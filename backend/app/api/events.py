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
    response_model=schemas.EventOut,
    status_code=status.HTTP_201_CREATED)
async def event_post(
    schema: schemas.EventIn,
    user: Optional[models.User] = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database)
) -> models.Event:
    """Create new event with POST request"""

    new_object = models.Event(**schema.dict())
    return await new_object.save(db_session)


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.EventOut)
async def event_get(
    id: int,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Event:
    """Retrieve event with GET request"""

    get_object = await models.Event.get(db_session, id=id)
    return get_object


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def event_delete(
    id: int,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Event:
    """Retrieve event with GET request"""

    get_object = await models.Event.get(db_session, id=id)
    return await get_object.delete(db_session)


@router.patch(
    path='/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.EventOut)
async def event_patch(
    id: int,
    schema: schemas.EventIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Event:
    """Modify event with PATCH request"""

    get_object = await models.Event.get(db_session, id=id)
    return await get_object.update(db_session, **schema.dict())


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.EventOut])
async def events_list(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    name: Optional[str] = FilterQuery,
):
    """List events with GET request"""

    return await models.Event.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        name=name,
    )


add_pagination(router)
