from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from . import auth_service, get_database, models, schemas

router = APIRouter()


@router.post(
    '/signup',
    response_model=schemas.SignupOut,
    status_code=201,
    tags=['signups'])
async def signup_post(schema: schemas.SignupIn,
                      db: Session = Depends(get_database)):
    """Generate new signup with POST request"""

    async def create():
        new_object = models.Signup(**schema.dict())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        return new_object
    return await create()


@router.get('/signup/{id}', response_model=schemas.SignupIn, tags=['signups'])
async def signup_get(
        id: int,
        db: Session = Depends(get_database),
        token: str = Depends(auth_service.oauth2_scheme)):
    """Retrieve signups object with GET request"""

    result = db.query(models.Signup).filter(models.Signup.id == id).first()
    if not result:
        detail = f'Signup with id {id} was not found'
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return result


@router.get(
    '/signups',
    response_model=LimitOffsetPage[schemas.SignupOut],
    tags=['signups'])
async def signups_list(
        db: Session = Depends(get_database),
        # token: str = Depends(auth_service.oauth2_scheme),
):
    """List signups with GET request"""
    return paginate(db.query(models.Signup).order_by(models.Signup.id.desc()))

add_pagination(router)
