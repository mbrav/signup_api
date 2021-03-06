import logging
from typing import Any, Dict

from aiogram import Bot, types
from app.config import settings
from fastapi import APIRouter, BackgroundTasks, Body, Response, status

from .commands import set_bot_commands
from .handlers import dp
from .loader import bot

router = APIRouter()
logger = logging.getLogger()


async def feed_update(update: Dict[str, Any]) -> None:
    telegram_update = types.Update(**update)
    if settings.WEBHOOK_USE:
        await dp.feed_webhook_update(bot, telegram_update)
    else:
        await dp.feed_update(bot, telegram_update)


@router.post(path='')
async def telegram_post(background_tasks: BackgroundTasks, update: Dict[str, Any] = Body(...)) -> Response:
    background_tasks.add_task(feed_update, update)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.on_event('startup')
async def on_startup() -> None:
    logging.info('Telegram bot startup')
    Bot.set_current(bot)
    await set_bot_commands(bot)
    if settings.WEBHOOK_USE:
        current_webhook = await bot.get_webhook_info()
        if current_webhook.url != settings.WEBHOOK_PATH:
            await bot.set_webhook(
                url=settings.WEBHOOK_URL,
                certificate=settings.SSL_PUBLIC)
    else:
        bot.get_updates()
    await bot.send_message(settings.TELEGRAM_ADMIN, '🤖🟢Signup Bot Startup')


@router.on_event('shutdown')
async def on_shutdown() -> None:
    logging.info('Telegram bot shutdown')
    await bot.send_message(settings.TELEGRAM_ADMIN, '🤖🔴Signup Bot Shutdown')
    await bot.delete_webhook()
