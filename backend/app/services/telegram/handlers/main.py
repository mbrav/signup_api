from aiogram import F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.config import settings

from .. import texts
from ..keyboards import me_keyboard, pagination_keyboard
from ..loader import bot, dp
from .handlers import (events_page, user_profile, user_registration,
                       user_signup_count, user_signup_page)
from .states import BotState


@dp.message(Command(commands=['start']))
@dp.message(F.text.in_({'start', 'begin'}))
async def start(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await bot.send_sticker(
        message.from_user.id,
        sticker=(texts.lotus_sheep))
    await message.reply(
        texts.ru.start_text.format(version=settings.VERSION))


@dp.message(Command(commands=['register']))
@dp.message(F.text.in_({'register', 'login'}))
async def register(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await user_registration(message)


@dp.message(Command(commands=['help']))
@dp.message(F.text.in_({'help', 'fuck'}))
async def help(message: types.Message, state: FSMContext):
    user_info = message.from_user
    await state.set_state(None)
    await message.reply(
        texts.ru.help_text_extra.format(
            first_name=user_info.first_name,
            last_name=user_info.first_name,
            username=user_info.username,
            lang=user_info.language_code,
            id=user_info.id))


@dp.message(Command(commands=['events']))
@dp.message(F.text.in_({'events', 'calendar'}))
async def events(message: types.Message, state: FSMContext):
    page = await events_page()

    await state.set_state(BotState.page_view)
    await state.update_data(page.dict())

    await bot.send_message(
        message.chat.id,
        page.text,
        reply_markup=pagination_keyboard(
            ids=page.elements_ids))


@dp.message(Command(commands=['me']))
@dp.message(F.text.in_({'me', 'my'}))
async def me(message: types.Message, state: FSMContext):

    await state.set_state(BotState.me_view)

    user = await user_profile(message)
    signup_count = await user_signup_count(user.id)

    await bot.send_message(
        message.chat.id,
        texts.ru.my_account.format(signup_count=signup_count),
        reply_markup=me_keyboard(action=None))
