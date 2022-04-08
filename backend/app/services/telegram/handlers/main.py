from aiogram import F, types
from aiogram.dispatcher.fsm.context import FSMContext
from app.config import settings

from .. import texts
from ..keyboards import signup_keyboard
from ..loader import bot, dp
from . import handlers, states


@dp.message(commands=['start'])
@dp.message(F.text.in_({'start', 'begin'}))
async def start(message: types.Message):
    await message.reply(
        texts.start_text.format(version=settings.VERSION))


@dp.message(commands=['register'])
@dp.message(F.text.in_({'register', 'login'}))
async def register(message: types.Message):
    await handlers.user_registration(message)


@dp.message(commands=['help'])
@dp.message(F.text.in_({'help', 'fuck'}))
async def help(message: types.Message):
    user_info = message.from_user

    await message.reply(
        texts.help_text_extra.format(
            first_name=user_info.first_name,
            last_name=user_info.first_name,
            username=user_info.username,
            lang=user_info.language_code,
            id=user_info.id))


@dp.message(commands=['events'])
@dp.message(F.text.in_({'events', 'calendar'}))
async def events(message: types.Message, state: FSMContext):
    page = await handlers.events_page()
    await state.set_state(states.PaginationState)
    await state.update_data(
        name='events',
        page_total=page.page_total,
        page_current=page.page_current,
        elements_total=page.elements_total)

    await state.update_data(previous_state=None)
    await state.update_data(previous_state=await state.get_state())

    await bot.send_message(
        message.chat.id,
        page.text,
        reply_markup=signup_keyboard)


@dp.callback_query(F.data.startswith('inline_page_'))
async def inline_pagination(call: types.CallbackQuery, state: FSMContext):
    passed_state = await state.get_data()

    page_current = passed_state.get('page_current', 1)
    page_total = passed_state.get('page_total', 1)
    # elements_total = passed_state.get('elements_total', 1)
    name = passed_state.get('name', None)

    if call.data == 'inline_page_left' and page_current > 1:
        page_current -= 1
    if call.data == 'inline_page_center':
        page_current = 1
    if call.data == 'inline_page_right' and page_current < page_total:
        page_current += 1

    await state.update_data(page_current=page_current)
    await state.update_data(previous_state=None)
    await state.update_data(previous_state=await state.get_state())

    reply_markup, page = None, None
    if name == 'events':
        page = await handlers.events_page(page_current)
        reply_markup = signup_keyboard

    if not page:
        return await bot.send_message(
            call.from_user.id,
            texts.inline_fail)

    await call.message.edit_text(
        page.text,
        reply_markup=reply_markup)


@dp.callback_query(F.data.startswith('inline_option_'))
async def inline_option_detail(
        call: types.CallbackQuery,
        state: FSMContext):

    selected_option = int(call.data.replace('inline_option_', ''))

    await call.message.edit_text(
        f'Selected option: {selected_option}',
        reply_markup=None)
