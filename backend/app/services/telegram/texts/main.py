start_text = (
    'Hi!\n'
    'This is signup_api {version}!\n'
    'Powered by aiogram.')

help_text = (
    '<b>Available Commands:</b>\n'
    '/start - Begin bot\n'
    '/help - Get help info\n'
    '/register - Register\n'
    '/signup - Signup\n')

help_text_extra = help_text + (
    '\n'
    '<b>Info about you:</b>\n'
    '🔸First Name: <code>{first_name}</code>\n'
    '🔸Last Name: <code>{last_name}</code>\n'
    '🔸Username: <code>{username}</code>\n'
    '🔸Locale <code>{lang}</code>\n'
    '🔸id: <code>{id}</code>\n')

register_create = 'Creating new account ...'

register_success = 'Hello {username}, you are now registered!'

register_already = 'Hello {username}, you are already registered!'

register_fail = (
    'There was an error with creating a new account\n'
    'Please contact support')
