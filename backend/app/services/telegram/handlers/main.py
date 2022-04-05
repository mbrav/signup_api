from aiogram import types
from app import models, schemas
from app.config import settings
from app.db import Session

from .. import texts
from ..keyboards import start_keyboard
from ..loader import bot, dp


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply(
        texts.start_text.format(version=settings.VERSION),
        reply_markup=start_keyboard)


@dp.message_handler(commands='register')
async def register(message: types.Message):

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


@dp.message_handler(commands='signup')
async def signup(message: types.Message):
    user_info = message.from_user
    await bot.send_message(
        settings.TELEGRAM_ADMIN,
        f'Signup: {user_info.username}')


@dp.message_handler(commands='help')
async def help(message: types.Message):
    user_info = message.from_user

    await message.reply(
        texts.help_text_extra.format(
            first_name=user_info.first_name,
            last_name=user_info.first_name,
            username=user_info.username,
            lang=user_info.language_code,
            id=user_info.id,
        ))
