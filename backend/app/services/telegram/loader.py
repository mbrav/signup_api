from aiogram import Bot, Dispatcher
from app.config import settings

bot = Bot(
    token=settings.TELEGRAM_TOKEN.get_secret_value(),
    parse_mode='HTML'
)

dp = Dispatcher()
