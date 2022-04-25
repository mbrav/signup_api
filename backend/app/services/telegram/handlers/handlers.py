
import asyncio
from datetime import datetime
from typing import Union

from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from app import models, schemas
from app.config import settings
from app.db import Session

from .. import texts
from ..keyboards import emoji_num
from ..loader import bot
from .states import Page


def time_text(dt: datetime, time_only=False):
    if time_only:
        return dt.strftime('%H:%M')
    return dt.strftime('%A, %-d %B %H:%M')


# GENERAL HANDLER FUNCTIONS

async def get_valid_state(call: types.CallbackQuery, state: FSMContext) -> FSMContext:
    """Check for expiration validity of a callback

    If not valid, create a countdown destruction of the the message.

    TODO: Investigate whether the asyncio.sleep function causes a delay for the
    the whole loop and not just the user. Ideally, it should not cause a delay
    for either.

    Args:
        call (types.CallbackQuery): Inline call of the current context
        state (FSMContext): Finite state machine context

    Returns:
        FSMContext: Return the context
    """
    passed_state = await state.get_data()
    if not passed_state:
        seconds = 5
        while seconds > 0:
            await call.message.edit_text(
                texts.inline_expired_destroy.format(seconds=seconds),
                reply_markup=None)
            await asyncio.sleep(1)
            seconds -= 1
        await call.message.delete()
    return passed_state


# USER HANDLERS

async def _user_get_or_create(
    message: Union[types.Message, types.CallbackQuery],
    registration: bool = False
) -> Union[None, models.Signup]:
    """Get or register new user

    Args:
        message (Union[types.Message, types.CallbackQuery]):
            Incoming message or callback to work with
        registration (bool, optional): Registration process. Defaults to False.

    Returns:
        Union[None, models.Signup]: Returns None or user
    """

    async with Session() as db_session:
        user = await models.User.get(
            db_session, tg_id=message.from_user.id, raise_404=False)

        if registration:
            if user:
                return await message.reply(
                    texts.register_already.format(
                        username=message.from_user.username))
            await bot.send_message(
                message.from_user.id, texts.register_create)

            username = str(message.from_user.id) if not (
                message.from_user.username) else message.from_user.username
            schema = schemas.UserCreateTg(
                username=username,
                tg_id=message.from_user.id,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name)
            new_user = models.User(**schema.dict())

            try:
                created_user = await new_user.save(db_session)
                await bot.send_message(
                    message.from_user.id,
                    texts.register_success.format(
                        username=created_user.username))
                await bot.send_message(
                    settings.TELEGRAM_ADMIN,
                    f'New user: {username}')
            except Exception as ex:
                await bot.send_message(
                    message.from_user.id,
                    texts.register_fail)
                await bot.send_message(
                    settings.TELEGRAM_ADMIN,
                    f'Error creating account\n {repr(ex)}')
            return

    if not user:
        return await bot.send_message(
            message.from_user.id,
            texts.register_not)
    return user


async def user_registration(message: types.Message) -> None:
    await _user_get_or_create(message, registration=True)


async def user_profile(message: Union[types.Message, types.CallbackQuery]) -> models.User:
    return await _user_get_or_create(message)


async def user_signup_count(user_id: int) -> int:
    # TODO: implement a more efficient query for object count
    async with Session() as db_session:
        signups = await models.Signup.by_user(db_session, user_id)
        return len(signups)


# EVENTS HANDLERS

async def event_detail(id: int) -> Page:
    async with Session() as db_session:
        db_result = await models.Event.get(db_session, id=id, raise_404=False)
    return db_result


async def events_page(page_current: int = 1, limit: int = 10) -> Page:
    """Generate paginated event list

    Args:
        page_current (int, optional): Current page view. Defaults to 1.
        limit (int, optional): Limit the number of elements per page. Defaults to 10.

    Returns:
        Page: dataclass to set the State
    """

    offset = (limit*page_current)-limit
    async with Session() as db_session:
        db_events = await models.Event.get_current(
            db_session, limit=limit, offset=offset)

        elements_total = await models.Event.get_current_count(db_session)
        pages_total = (elements_total // limit) + 1

    text = texts.events_page_body.format(
        page_current=page_current,
        pages_total=pages_total,
        elements_total=elements_total)

    event_ids = []
    for index, event in enumerate(db_events):
        event_ids.append(event.id)
        text += texts.events_page_detail.format(
            index=emoji_num[index+1],
            name=event.name,
            start=time_text(event.start),
            end=time_text(event.end, True))

    return Page(text=text,
                name='events',
                pages_total=pages_total,
                page_current=page_current,
                elements_total=elements_total,
                elements_ids=event_ids)


# SIGNUPS HANDLERS

async def user_signup_page(call: types.CallbackQuery) -> str:
    """Generate paginated signup list by user id
    """

    user = await user_profile(call)
    async with Session() as db_session:
        db_signups = await models.Signup.by_user(db_session, user.id)
        elements_total = len(db_signups)

    text = texts.my_signups.format(
        signup_count=elements_total)

    for index, signup in enumerate(db_signups):
        text += texts.signups_page_detail.format(
            index=emoji_num[index+1],
            name=signup.event.name,
            start=time_text(signup.event.start),
            end=time_text(signup.event.end, True))
    return text


async def _get_or_create_signup(call: types.CallbackQuery, event_id: int) -> Union[bool, models.Signup]:
    """Get or create new signup

    Args:
        call (types.CallbackQuery): Inline call of the current context
        event_id (int): Id of the event in the db table

    Returns:
        Union[bool, models.Signup]: False or model
    """

    async with Session() as db_session:
        try:
            user = await models.User.get(
                db_session, tg_id=call.from_user.id, raise_404=False)
        except Exception:
            await call.message.edit_text(
                texts.register_not,
                reply_markup=None)
            return False
        try:
            event = await models.Event.get(db_session, id=event_id)
        except Exception:
            await call.message.edit_text(
                texts.inline_fail,
                reply_markup=None)
            return False

        get_signup = await models.Signup.get_list(
            db_session=db_session,
            one=True,
            user_id=user.id,
            event_id=event.id)

        if get_signup:
            return get_signup

        new_signup = models.Signup(user_id=user.id, event_id=event.id)
        await new_signup.save(db_session)
        return new_signup


async def signup_create(call: types.CallbackQuery, event_id: int) -> models.Signup:
    return await _get_or_create_signup(call, event_id)


async def signup_cancel(call: types.CallbackQuery, event_id: int) -> None:
    # TODO Add time check or add cancel attribute to model
    get_signup = await _get_or_create_signup(call, event_id)
    async with Session() as db_session:
        await get_signup.delete(db_session)
