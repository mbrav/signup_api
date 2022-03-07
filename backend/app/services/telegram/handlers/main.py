from aiogram import types

from ..loader import dp

# from app.models import User


@dp.message_handler(commands='start')
async def start(message: types.Message):
    # if await User.exists(tg_id=message.chat.id) is False:
    #     await User.create(tg_id=message.chat.id,
    #                       first_name=message.chat.first_name,
    #                       last_name=message.chat.last_name,
    #                       tg_username=message.chat.username,
    #                       is_admin=True)
    #     return await message.reply(f'Hello new user {message.chat.username}!')
    await message.reply('Hello world!')
