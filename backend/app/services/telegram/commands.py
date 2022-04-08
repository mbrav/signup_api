
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from . import texts


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description=texts.command1_detail),
        BotCommand(
            command='help',
            description=texts.command2_detail),
        BotCommand(
            command='register',
            description=texts.command3_detail),
        BotCommand(
            command='events',
            description=texts.command4_detail)]
    await bot.set_my_commands(
        commands=commands, scope=BotCommandScopeAllPrivateChats())
