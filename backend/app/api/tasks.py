from typing import Dict, Optional

from app import db, models, schemas
from app.services import TaskDetail, tasks_info
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_pagination import LimitOffsetPage, add_pagination
from sqlalchemy.ext.asyncio import AsyncSession

from .deps import (FilterQuery, SortByDescQuery, SortByQuery,
                   get_active_superuser, get_active_user)

router = APIRouter()


async def check_method(name: str, kwargs: dict):
    """Check if method is available"""

    if name not in tasks_info.keys():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': f'Function {name} is not available.',
                    'methods': tasks_info})

    arguments = tasks_info[name]['arguments']
    if len(kwargs) != len(arguments):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'error': f'Incorrect number of arguments passed for {name}. '
                    f'Passed: {len(kwargs)}, required: {len(arguments)}',
                    'arguments': arguments})


@router.get(
    path='/available',
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, TaskDetail])
async def available_tasks_list(
    db_session: AsyncSession = Depends(db.get_database),
):
    """List executable tasks with GET request"""

    return tasks_info


@router.post(
    path='',
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED)
async def task_post(
    schema: schemas.TaskIn,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Create new task with POST request"""

    await check_method(schema.name, schema.kwargs)
    new_object = models.Task(**schema.dict(), user_id=user.id)
    return await new_object.save(db_session)


@router.post(
    path='/{id}/abort',
    response_model=schemas.TaskOut,
    status_code=status.HTTP_201_CREATED)
async def task_abort(
    id: int,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Abort task with POST request"""

    get_object = await models.Task.get(db_session, id=id)
    await get_object.abort()
    updated = schemas.TaskUpdate(**get_object.__dict__)
    return await get_object.update(db_session, **updated.__dict__)


@router.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TaskOut)
async def task_get(
    id: int,
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Retrieve task with GET request"""

    get_object = await models.Task.get(db_session, id=id)
    return get_object


@router.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT)
async def task_delete(
    id: int,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Retrieve task with GET request"""

    get_object = await models.Task.get(db_session, id=id)
    return await get_object.delete(db_session)


@router.patch(
    path='/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.TaskOut)
async def task_patch(
    id: int,
    schema: schemas.TaskIn,
    user: models.User = Depends(get_active_superuser),
    db_session: AsyncSession = Depends(db.get_database),
) -> models.Task:
    """Modify task with PATCH request"""

    await check_method(schema.name, schema.kwargs)
    get_object = await models.Task.get(db_session, id=id)
    await get_object.update_planned_for(schema.delay_seconds)
    updated = schemas.TaskUpdate(**get_object.__dict__)
    return await get_object.update(db_session, **updated.__dict__)


@router.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.TaskOut])
async def tasks_list(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    user_id: Optional[int] = FilterQuery,
    status: Optional[str] = FilterQuery,
    result: Optional[str] = FilterQuery,
):
    """List tasks with GET request"""

    return await models.Task.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        user_id=user_id,
        status=status,
        result=result
    )


@router.get(
    path='/my',
    status_code=status.HTTP_200_OK,
    response_model=LimitOffsetPage[schemas.TaskOut])
async def tasks_list_by_user(
    user: models.User = Depends(get_active_user),
    db_session: AsyncSession = Depends(db.get_database),
    sort_by: Optional[str] = SortByQuery,
    desc: Optional[bool] = SortByDescQuery,
    status: Optional[str] = FilterQuery,
    result: Optional[str] = FilterQuery,
):
    """List tasks of user with GET request"""

    return await models.Task.paginate(
        db_session,
        desc=desc,
        sort_by=sort_by,
        user_id=user.id,
        status=status,
        result=result
    )

add_pagination(router)
