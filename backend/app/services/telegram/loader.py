from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app.config import settings

bot = Bot(
    token=settings.TELEGRAM_TOKEN.get_secret_value(),
    parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
