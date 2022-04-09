from aiogram import F, types
from aiogram.dispatcher.fsm.context import FSMContext
from app.config import settings

from .. import texts
from ..keyboards import pagination_keyboard, signup_detail_nav
from ..loader import bot, dp
from . import handlers, states


@dp.message(commands=['start'])
@dp.message(F.text.in_({'start', 'begin'}))
async def start(message: types.Message):
    await bot.send_sticker(
        message.from_user.id,
        sticker=('CAACAgIAAxkBAAIFimJRkWrfmVcBUTeqLQ'
                 'O0cC9N885dAAJuAAPkoM4HJzcoIDg3bXsjBA'))
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
        elements_total=page.elements_total,
        elements_id_dict=page.elements_id_dict)

    await state.update_data(previous_state=None)
    await state.update_data(previous_state=await state.get_state())

    await bot.send_message(
        message.chat.id,
        page.text,
        reply_markup=pagination_keyboard(options=len(page.elements_id_dict)))


@dp.callback_query(F.data.startswith('inline_page_'))
async def inline_pagination(call: types.CallbackQuery, state: FSMContext):
    passed_state = await handlers.get_valid_state(call, state)
    if not passed_state:
        return

    page_current = passed_state.get('page_current', 1)
    name = passed_state.get('name', None)

    if call.data == 'inline_page_left' and page_current > 1:
        page_current -= 1
    if call.data == 'inline_page_center':
        page_current = 1
    if call.data == 'inline_page_right' and (
            page_current < passed_state.get('page_total')):
        page_current += 1

    reply_markup, page = None, None
    if name == 'events':
        page = await handlers.events_page(page_current)
        reply_markup = pagination_keyboard(
            options=len(page.elements_id_dict))

    if not page:
        return await bot.send_message(
            call.from_user.id,
            texts.inline_fail)

    await state.update_data(page_current=page_current)
    await state.update_data(elements_id_dict=page.elements_id_dict)
    await state.update_data(previous_state=None)
    await state.update_data(previous_state=await state.get_state())

    await call.message.edit_text(
        page.text,
        reply_markup=reply_markup)


@dp.callback_query(F.data.startswith('inline_option_'))
async def inline_option_detail(
    call: types.CallbackQuery,
    state: FSMContext
):
    passed_state = await handlers.get_valid_state(call, state)
    if not passed_state:
        return

    option_id = int(call.data.replace('inline_option_', ''))
    id_dict = passed_state.get('elements_id_dict', {})
    element_id = id_dict.get(option_id, None)
    name = passed_state.get('name', None)

    reply_markup, detail = None, None
    if name == 'events':
        detail = await handlers.event_detail(id=element_id)
        reply_markup = signup_detail_nav(
            selected=False, notification=False)

    if not detail:
        return await bot.send_message(
            call.from_user.id,
            texts.inline_fail)

    await call.message.edit_text(
        texts.events_detail.format(
            name=detail.name,
            start=handlers.time_text(detail.end),
            end=handlers.time_text(detail.start, True)),
        reply_markup=reply_markup)
