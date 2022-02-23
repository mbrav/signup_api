from app import db, models, schemas
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

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

    db_session: Session = Depends(db.get_database)
) -> models.Signup:
    """Generate new signup with POST request"""

    # Instead of this
    model = models.Signup

    async def create():
        new_object = model(**schema.dict())
        db_session.add(new_object)
        db_session.commit()
        db_session.refresh(new_object)
        return new_object
    return await create()


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.SignupOut)
async def signup_get(
    id: int,
    db_session: Session = Depends(db.get_database),
    token: str = Depends(auth_service.oauth2_scheme)
) -> models.Signup:
    """Retrieve signups object with GET request"""

    model = models.Signup
    get_object = db_session.query(model).filter(model.id == id).first()
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
    token: str = Depends(auth_service.oauth2_scheme),
    user: models.User = Depends(get_active_user),
    db_session: Session = Depends(db.get_database)
):
    """List signups with GET request"""

    model = models.Signup
    return paginate(db_session.query(model).order_by(model.id.desc()))


add_pagination(router)
