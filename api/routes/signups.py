from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from . import auth, get_database, models, schemas

router = APIRouter()


@router.get('/', tags=['index'])
async def index(message: str = None):
    """Index Function

    Args:
        message: Message to the server

    Returns:
        message: Message to the server
        response: Message from the server
        time: Server Time

    """

    response = {
        'message': f'{message}',
        'response': 'Fast API service for signups and Telegram integration',
        'time': datetime.utcnow().isoformat()
    }
    return response


@router.post(
    '/signup',
    response_model=schemas.SignupOut,
    status_code=201,
    tags=['signups'])
async def signup_post(schema: schemas.SignupIn, db: Session = Depends(get_database)):
    """Generate new signup with POST request"""

    async def create():
        new_object = models.Signup(**schema.dict())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)
        return new_object
    return await create()


@router.get('/signup/{id}', response_model=schemas.SignupOut, tags=['signups'])
async def signup_get(
        id: int,
        db: Session = Depends(get_database),
        token: str = Depends(auth.oauth2_scheme)):
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
        token: str = Depends(auth.oauth2_scheme)):
    """List signups with GET request"""
    return paginate(db.query(models.Signup))

add_pagination(router)
