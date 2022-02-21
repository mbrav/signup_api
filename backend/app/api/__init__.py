from fastapi import APIRouter

from . import auth, index, signups, users
from .auth import auth_service

api_router = APIRouter()
api_router.include_router(index.router, tags=['Index'])
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
api_router.include_router(signups.router, prefix='/signups', tags=['Signups'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
