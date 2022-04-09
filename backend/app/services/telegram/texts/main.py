command1_detail = 'Begin bot'
command2_detail = 'Get help info'
command3_detail = 'Register new account'
command4_detail = 'Get current list of events'

help_text = f"""
<b>Available Commands:</b>
/start - {command1_detail}
/help - {command2_detail}
/register - {command3_detail}
/events - {command4_detail}
"""

help_text_extra = help_text + """
<b>Info about you:</b>
🔸First Name: <code>{first_name}</code>
🔸Last Name: <code>{last_name}</code>
🔸Username: <code>{username}</code>
🔸Locale <code>{lang}</code>
🔸id: <code>{id}</code>
"""

start_text = """
🤖Hi!
This is signup_api v{version}!
Powered by aiogram
""" + help_text

register_create = '🤖Creating new account ...'

register_not = """
🤖You are not registered...
🔧Please register: /register
"""

register_success = 'Hello {username}, you are now registered!'

register_already = 'Hello {username}, you are already registered!'

register_fail = """
🤖There was an error with creating a new account
🔧Please contact support
"""

inline_fail = """
🤖Sorry, bot\s logic has malfunctioned
🔧Please start again: /start
"""

inline_expired = """
🤖Sorry, the following message has expired
🔧Please start again: /start
"""

inline_expired_destroy = inline_expired + """
🗑️<i>The following message will self-destruct in {seconds} seconds.</i>
"""

events_page_body = """
<b>Page:</b> {page_current}/{page_total}
<b>Events: {elements_total}</b>
"""

events_page_detail = """
<b>{index}</b> - <i>{name}</i>
{start} - {end}
"""

events_detail = """
<i>{name}</i>
{start} - {end}
"""
