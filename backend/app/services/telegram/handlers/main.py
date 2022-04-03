from aiogram import types
from app import models, schemas
from app.db import Session

from ..loader import bot, dp


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.reply("Hi!\nI'm a signup Bot !\nPowered by aiogram.")


@dp.message_handler(commands='register')
async def register(message: types.Message):

    async with Session() as db_session:
        user = await models.User.get(
            db_session, tg_id=message.from_user.id, raise_404=False)

        if user:
            return await message.reply(f'Hello {user.username}!')

        await message.reply('Creating a new account ...')

        schema = schemas.UserCreateTg(
            username=message.from_user.username,
            tg_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name)

        new_user = models.User(**schema.dict())
        created_user = await new_user.save(db_session)
        await message.reply(f'Hello {created_user.username}, you are now registered!')


@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)
