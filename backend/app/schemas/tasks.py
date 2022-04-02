
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

example_kwargs = {
    'text': 'hello',
    'text2': 'world',
}


class TaskStatus(str, Enum):
    created = 'created'
    aborted = 'aborted'
    expired = 'expired'
    rescheduled = 'rescheduled'
    queued = 'queued'
    processing = 'processing'
    completed = 'completed'
    error = 'error'


class TaskIn(BaseModel):

    name: str = Field(
        example='combine',
        description='Valid function name')
    kwargs: Optional[dict] = Field(
        example=example_kwargs,
        description='Qwargs to pass into function')
    delay_seconds: int = Field(
        example=10,
        description='Delay in seconds since creation of task')

    class Config:
        orm_mode = True


class TaskUpdate(TaskIn):
    status: TaskStatus = TaskStatus.queued
    completed_at: Optional[datetime]


class TaskOut(TaskIn):
    status: TaskStatus = TaskStatus.created
    result: Optional[str] = Field(example=None)
    created_at: datetime
    updated_at: Optional[datetime]
    planned_for: Optional[datetime]
    completed_at: Optional[datetime]
    user_id: int = Field(example=1)
    id: int = Field(example=1)
