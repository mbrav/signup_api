from enum import Enum

from aiogram.dispatcher.filters.callback_data import CallbackData


class PageNav(str, Enum):
    left = 'left'
    center = 'center'
    right = 'right'


class Action(str, Enum):
    back = 'back'
    signup = 'signup'
    signup_cancel = 'signup_cancel'
    notify_toggle = 'notify_toggle'
    signups = 'signups'
    account = 'account'
    settings = 'settings'


class BaseCallback(CallbackData, prefix=''):
    option_id: int = None
    action: Action = None
    page_nav: PageNav = None


class MeCallback(BaseCallback, prefix='me'):
    pass


class EventCallback(BaseCallback, prefix='event'):
    pass
