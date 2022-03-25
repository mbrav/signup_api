from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import get_active_user

router = APIRouter()


@router.post(
    path='',
    response_model=schemas.SignupOut,
    status_code=status.HTTP_201_CREATED)
async def signup_post(
    schema: schemas.SignupCreate,
    db_session: AsyncSession = Depends(db.get_database)
) -> models.Signup:
    """Generate new signup with POST request"""

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
    """Retrieve signups object with GET request"""

    get_object = await models.Signup.get(db_session, id=id)

    if not get_object:
        detail = f'Signup with id {id} was not found'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return get_object


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.SignupOut])
async def signups_list(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database)
):
    """List signups with GET request"""

    from sqlalchemy import select

    model = models.Signup

    stmt = select(model).order_by(model.id.desc())
    result = await db_session.execute(stmt)
    get_objects = result.scalars().all()

    # Fix pagination
    return paginate(result)


add_pagination(router)
