
from datetime import datetime

from aiogram import types
from app import models, schemas
from app.config import settings
from app.db import Session

from .. import texts
from ..keyboards import emoji_num
from ..loader import bot
from .states import Page


def time_text(dt: datetime):
    return dt.strftime('%d/%m/%Y, %H:%M')


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
        db_result = await models.Event.get_current(
            db_session, limit=limit, offset=offset)
        db_events = db_result.scalars().all()
        db_all = await models.Event.get_current(db_session)

        # TODO: optimize db query to get count instead of objects
        elements_total = len(db_all.scalars().all())
        page_total = elements_total // limit + 1

    text = texts.events_page_body.format(
        page_current=page_current,
        page_total=page_total,
        elements_total=elements_total)

    for index, event in enumerate(db_events):
        text += texts.events_page_detail.format(
            index=emoji_num[index+1],
            name=event.name,
            start=time_text(event.start))
    return Page(text, page_total, page_current, elements_total)
