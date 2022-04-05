import logging
from asyncio import get_event_loop
from typing import Any

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

logger = logging.getLogger(__name__)
dp = Dispatcher()


@dp.message(commands={'start'})
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    # Most of event objects has an aliases for API methods to be called in event context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage` method automatically
    # or call API method directly via Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f'Привет, <b>{message.from_user.full_name}!</b>')


@dp.message()
async def echo_handler(message: types.Message) -> Any:
    """
    Handler will forward received message back to the sender

    By default message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('Nice try!')


class TGbot():
    """Bot class"""

    def __init__(self, token: str):
        """Init bot with API key"""
        self.bot = Bot(token=token, parse_mode='HTML')

    def run(self) -> None:
        logger.info('Starting bot')
        dp.run_polling(self.bot, loop=get_event_loop())
