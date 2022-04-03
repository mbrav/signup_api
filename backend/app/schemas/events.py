from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class EventIn(BaseModel):
    name: str = Field(example='Chinese Beginner Lesson')
    description: str = Field(example='We will learn what 你好 means')
    start: datetime = Field(example=datetime.utcnow())
    end: Optional[datetime] = Field(example=datetime.utcnow())
    google_id: Optional[str] = Field(example='35co6foa8b73hnavn5qf1dpuek')

    class Config:
        orm_mode = True


class EventCalIn(EventIn):
    google_modified: Optional[datetime]


class EventOut(EventCalIn):
    created_at: datetime
    id: int = Field(example=1)
