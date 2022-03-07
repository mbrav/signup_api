from asyncio import get_event_loop

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.config import settings

bot = Bot(
    settings.TELEGRAM_BOT_API_KEY,
    parse_mode=types.ParseMode.HTML
)

dp = Dispatcher(
    bot=bot,
    storage=MemoryStorage(),
    loop=get_event_loop()
)
