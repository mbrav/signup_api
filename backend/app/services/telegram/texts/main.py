command1_detail = 'Begin bot'
command2_detail = 'Get help info'
command3_detail = 'Register new account'
command4_detail = 'Get current list of events'

help_text = (
    '<b>Available Commands:</b>\n'
    f'/start - {command1_detail}\n'
    f'/help - {command2_detail}\n'
    f'/register - {command3_detail}\n'
    f'/events - {command4_detail}\n')

help_text_extra = help_text + (
    '\n'
    '<b>Info about you:</b>\n'
    '🔸First Name: <code>{first_name}</code>\n'
    '🔸Last Name: <code>{last_name}</code>\n'
    '🔸Username: <code>{username}</code>\n'
    '🔸Locale <code>{lang}</code>\n'
    '🔸id: <code>{id}</code>\n')

start_text = (
    'Hi!\n'
    'This is signup_api v{version}!\n'
    'Powered by aiogram\n'
    '\n') + help_text


register_create = 'Creating new account ...'

register_success = 'Hello {username}, you are now registered!'

register_already = 'Hello {username}, you are already registered!'

register_fail = (
    'There was an error with creating a new account\n'
    'Please contact support')

inline_fail = (
    'Sorry, bot\'s logic has malfunctioned\n'
    'Please start again: /start')

events_page_body = (
    '<b>Page:</b> {page_current}/{page_total}\n'
    '<b>Events: {elements_total}</b>\n')

events_page_detail = ('<b>{index}</b> - <i>{name}</i>\n'
                      '{start}\n\n')
