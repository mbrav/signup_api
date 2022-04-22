from typing import Optional

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

from . import texts
from .callbacks import Action, EventCallback, MeCallback, PageNav

emoji_num = [
    '0️⃣',
    '1️⃣',
    '2️⃣',
    '3️⃣',
    '4️⃣',
    '5️⃣',
    '6️⃣',
    '7️⃣',
    '8️⃣',
    '9️⃣',
    '🔟',
]

me_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=texts.inline_me_button_1,
                callback_data=MeCallback(
                    action=Action.signups).pack()),
            InlineKeyboardButton(
                text=texts.inline_me_button_2,
                callback_data=MeCallback(
                    action=Action.account).pack()),
            InlineKeyboardButton(
                text=texts.inline_me_button_3,
                callback_data=MeCallback(
                    action=Action.settings).pack()),
            # KeyboardButton(text=texts.inline_me_button_3,
            #                request_contact=True)
        ]
    ])

pagination_nav = [
    InlineKeyboardButton(
        text=texts.inline_signup_button_1,
        callback_data=EventCallback(page_nav=PageNav.left).pack()),
    InlineKeyboardButton(
        text=texts.inline_signup_button_2,
        callback_data=EventCallback(page_nav=PageNav.center).pack()),
    InlineKeyboardButton(
        text=texts.inline_signup_button_3,
        callback_data=EventCallback(page_nav=PageNav.right).pack())
]


def signup_detail_nav(
    id: int,
    selected: bool = False,
    notification: Optional[bool] = None,
) -> InlineKeyboardMarkup:
    """Generate signup detail based on states

    Args:
        id (int): id of the object to dispaly in inline context
        selected (bool, optional): Selected of not selected state. Defaults to False.
        notification (bool, optional): Pass state option notification state.
            Generates if either True or False. Defaults to None.

    Returns:
        InlineKeyboardMarkup: Generated keyboard
    """

    keys = [
        InlineKeyboardButton(
            text=texts.inline_signup_action_1,
            callback_data=EventCallback(page_nav=PageNav.center).pack())
    ]

    if selected:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_signup_action_3,
                callback_data=EventCallback(
                    action=Action.signup,
                    option_id=id).pack()))
    else:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_signup_action_2,
                callback_data=EventCallback(
                    action=Action.signup,
                    option_id=id).pack()))

    if notification is True:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_notify_on,
                callback_data=EventCallback(
                    action=Action.notify_toggle,
                    option_id=id).pack()))
    elif notification is False:
        keys.append(
            InlineKeyboardButton(
                text=texts.inline_notify_off,
                callback_data=EventCallback(
                    action=Action.notify_toggle,
                    option_id=id).pack()))
    keyboard = [keys]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def pagination_keyboard(
        ids: list,
        cols: int = 5
) -> InlineKeyboardMarkup:
    """Pagination keyboard generator algorithm based on pagination params"""

    # if cols > 8:
    #     # 8 is maximum number of buttons for telegram
    #     cols = 8

    # pages = options // cols
    # remainder = options % cols

    # keyboard = []
    # index = 1
    # while index <= options:
    #     if options <= 10:
    #         i = 0
    #         if index < 5:
    #             i = 1
    #         # keyboard[i].append(
    #         #     InlineKeyboardButton(
    #         #         text=emoji_num[index],
    #         #         callback_data=f'inline_events_option_{index}'))
    #         keyboard.append(f'inline_events_option_{index}')
    #     else:
    #         pass
    #     index += 1

    # keyboard.append(pagination_nav)
    # return keyboard

    keyboard = [
        [
            InlineKeyboardButton(
                text=emoji_num[1],
                callback_data=EventCallback(
                    option_id=ids[0]).pack()),
            InlineKeyboardButton(
                text=emoji_num[2],
                callback_data=EventCallback(
                    option_id=ids[1]).pack()),
            InlineKeyboardButton(
                text=emoji_num[3],
                callback_data=EventCallback(
                    option_id=ids[2]).pack()),
            InlineKeyboardButton(
                text=emoji_num[4],
                callback_data=EventCallback(
                    option_id=ids[3]).pack()),
            InlineKeyboardButton(
                text=emoji_num[5],
                callback_data=EventCallback(
                    option_id=ids[4]).pack()),
        ],
        [
            InlineKeyboardButton(
                text=emoji_num[6],
                callback_data=EventCallback(
                    option_id=ids[5]).pack()),
            InlineKeyboardButton(
                text=emoji_num[7],
                callback_data=EventCallback(
                    option_id=ids[6]).pack()),
            InlineKeyboardButton(
                text=emoji_num[8],
                callback_data=EventCallback(
                    option_id=ids[7]).pack()),
            InlineKeyboardButton(
                text=emoji_num[9],
                callback_data=EventCallback(
                    option_id=ids[8]).pack()),
            InlineKeyboardButton(
                text=emoji_num[10],
                callback_data=EventCallback(
                    option_id=ids[9]).pack()),
        ],
        pagination_nav
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
