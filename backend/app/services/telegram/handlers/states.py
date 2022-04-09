

from typing import Any, Optional

from aiogram.dispatcher.fsm.state import State, StatesGroup
from pydantic import BaseModel


class Page(BaseModel):
    text: Optional[str]
    name: Optional[str]
    pages_total: Optional[int]
    page_current: Optional[int]
    elements_total: Optional[int]
    elements_id_dict: Optional[dict]
    previous_state: Optional[Any]


class BotState(StatesGroup):
    page_view = State()
