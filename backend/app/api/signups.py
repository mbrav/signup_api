from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import auth_service, get_active_user

router = APIRouter()


@router.post(
    path='',
    response_model=schemas.SignupOut,
    status_code=status.HTTP_201_CREATED)
async def signup_post(
    schema: schemas.SignupCreate,

    # TODO Figure out how to pass a SQLachemy model as a dependency
    # See https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/
    # model: models.Signup = Depends(models.Signup),

    db_session: AsyncSession = Depends(db.get_database)
) -> models.Signup:
    """Generate new signup with POST request"""

    # Instead of this
    model = models.Signup

    new_object = model(**schema.dict())

    db_session.add(new_object)
    return await db_session.commit()

    # Fix error
    # greenlet_spawn has not been called; can't call await_() here.
    # Was IO attempted in an unexpected place?
    return new_object


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

    model = models.Signup

    stmt = select(model).where(model.id == id)
    result = await db_session.execute(stmt)
    get_object = result.scalars().first()

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

    model = models.Signup

    stmt = select(model).order_by(model.id.desc())
    result = await db_session.execute(stmt)
    get_objects = result.scalars().all()

    # Fix pagination
    return paginate(result)


add_pagination(router)
