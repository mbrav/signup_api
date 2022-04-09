
import asyncio
from datetime import datetime

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


async def user_registration(message: types.Message) -> None:
    async with Session() as db_session:
        user = await models.User.get(
            db_session, tg_id=message.from_user.id, raise_404=False)

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


async def events_page(page_current: int = 1, limit: int = 10) -> Page:
    offset = (limit*page_current)-limit
    async with Session() as db_session:
        db_events = await models.Event.get_current(
            db_session, limit=limit, offset=offset)

        elements_total = await models.Event.get_current_count(db_session)
        page_total = (elements_total // limit) + 1

    text = texts.events_page_body.format(
        page_current=page_current,
        page_total=page_total,
        elements_total=elements_total)

    event_ids = {}
    for index, event in enumerate(db_events):
        event_ids[index+1] = event.id
        text += texts.events_page_detail.format(
            index=emoji_num[index+1],
            name=event.name,
            start=time_text(event.start),
            end=time_text(event.end, True))
    return Page(text, page_total, page_current, elements_total, event_ids)


async def event_detail(id: int) -> Page:
    async with Session() as db_session:
        db_result = await models.Event.get(db_session, id=id, raise_404=False)
    return db_result


async def get_valid_state(call: types.CallbackQuery, state: FSMContext) -> types.Message:
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
