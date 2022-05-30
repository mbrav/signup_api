
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from . import texts


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description=texts.ru.command1_detail),
        BotCommand(
            command='help',
            description=texts.ru.command2_detail),
        BotCommand(
            command='register',
            description=texts.ru.command3_detail),
        BotCommand(
            command='events',
            description=texts.ru.command4_detail),
        BotCommand(
            command='me',
            description=texts.ru.command5_detail)]
    await bot.set_my_commands(
        commands=commands, scope=BotCommandScopeAllPrivateChats())
