from typing import Any, Dict

from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from app.config import settings
from fastapi import APIRouter, BackgroundTasks, Body, Response, status

from .handlers import dp
from .middlewares import ThrottlingMiddleware

tg_router = APIRouter()


async def feed_update(update: dict):
    telegram_update = Update(**update)
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    await dp.process_update(telegram_update)


@tg_router.post(path='')
async def telegram_post(background_tasks: BackgroundTasks, update: Dict[str, Any] = Body(...)) -> Response:
    background_tasks.add_task(feed_update, update)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@tg_router.on_event('startup')
async def on_startup() -> None:
    Bot.set_current(dp.bot)
    Dispatcher.set_current(dp)
    dp.middleware.setup(ThrottlingMiddleware())
    current_url = (await dp.bot.get_webhook_info())['url']
    if current_url != settings.WEBHOOK_PATH:
        await dp.bot.set_webhook(url=settings.WEBHOOK_URL)
    if not settings.DEBUG:
        await dp.bot.send_message(settings.ADMIN, 'Signup Bot.')


@tg_router.on_event('shutdown')
async def on_shutdown() -> None:
    await dp.storage.close()
    await dp.storage.wait_closed()
    await dp.bot.session.close()
