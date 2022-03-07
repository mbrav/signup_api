from aiogram import types

from ..loader import dp


@dp.message_handler(commands='hi')
async def start(message: types.Message):
    await message.reply(f'hi {message}')
