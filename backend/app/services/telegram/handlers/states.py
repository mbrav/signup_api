
from dataclasses import dataclass

from aiogram.dispatcher.fsm.state import State, StatesGroup


@dataclass
class Page:
    text: str
    page_total: int
    page_current: int
    elements_total: int
    elements_id_dict: dict


class PaginationState(StatesGroup):
    name = State()
    page_total = State()
    page_current = State()
    elements_total = State()
    previous_state = State()
    elements_current = State()
    id_dict = State()
