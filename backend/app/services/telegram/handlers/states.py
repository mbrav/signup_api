

from typing import Any, Optional

from aiogram.dispatcher.fsm.state import State, StatesGroup
from pydantic import BaseModel


class Page(BaseModel):
    text: Optional[str]
    name: Optional[str]
    pages_total: Optional[int]
    page_current: Optional[int]
    elements_ids: Optional[list]


class BotState(StatesGroup):
    page_view = State()
    account_view = State()
