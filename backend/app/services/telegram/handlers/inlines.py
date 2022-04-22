from aiogram import F, types
from aiogram.dispatcher.fsm.context import FSMContext

from .. import texts
from ..callbacks import Action, EventCallback, MeCallback, PageNav
from ..keyboards import me_keyboard, pagination_keyboard, signup_detail_nav
from ..loader import bot, dp
from .handlers import (event_detail, events_page, get_valid_state,
                       signup_create, time_text)


@dp.callback_query(EventCallback.filter(F.page_nav))
async def inline_pagination(call: types.CallbackQuery, state: FSMContext):
    passed_state = await get_valid_state(call, state)
    if not passed_state:
        return

    nav = EventCallback.unpack(call.data).page_nav
    page_current = passed_state.get('page_current', 1)

    if nav is PageNav.left and page_current > 1:
        page_current -= 1
    if nav is PageNav.center:
        page_current = 1
    if nav is PageNav.right and (
            page_current < passed_state.get('pages_total')):
        page_current += 1

    page = await events_page(page_current)
    reply_markup = pagination_keyboard(
        ids=page.elements_ids)

    if not page:
        return await bot.send_message(
            call.from_user.id,
            texts.inline_fail)

    await state.update_data(page_current=page_current)
    await state.update_data(elements_ids=page.elements_ids)

    await call.message.edit_text(
        page.text,
        reply_markup=reply_markup)


@dp.callback_query(EventCallback.filter(F.option_id))
async def inline_events_option(
    call: types.CallbackQuery,
    state: FSMContext
):
    passed_state = await get_valid_state(call, state)
    if not passed_state:
        return

    element_id = EventCallback.unpack(call.data).option_id
    action = EventCallback.unpack(call.data).action

    if action is Action.signup:
        result = await signup_create(call, element_id)
        if result is False:
            return

    reply_markup = signup_detail_nav(
        id=element_id, selected=False)

    detail = await event_detail(id=element_id)
    if not detail:
        return await bot.send_message(
            call.from_user.id,
            texts.inline_fail)

    await call.message.edit_text(
        texts.events_detail.format(
            name=detail.name,
            start=time_text(detail.end),
            end=time_text(detail.start, time_only=True)),
        reply_markup=reply_markup)


@dp.callback_query(MeCallback.filter(F.action))
async def inline_me(
    call: types.CallbackQuery,
    state: FSMContext
):
    passed_state = await get_valid_state(call, state)
    if not passed_state:
        return

    action = MeCallback.unpack(call.data).action

    await call.message.edit_text(
        texts.my_account.format(signup_count=action),
        reply_markup=me_keyboard)
