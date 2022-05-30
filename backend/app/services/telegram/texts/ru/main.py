command1_detail = 'Начать бот'
command2_detail = 'Получить помощь'
command3_detail = 'Регистрация'
command4_detail = 'Список занятий'
command5_detail = 'Моя учётная запись'

help_text = f"""
<b>Команды:</b>
/start - {command1_detail}
/register - {command2_detail}
/events - {command3_detail}
/me - {command4_detail}
/help - {command5_detail}
"""

help_text_extra = help_text + """
<b>Ваша информация:</b>
🔸Имя: <code>{first_name}</code>
🔸Фамилия: <code>{last_name}</code>
🔸Никнейм: <code>{username}</code>
🔸Код языка: <code>{lang}</code>
🔸id: <code>{id}</code>
"""

start_text = """
🤖Привет!
Это signup_api v{version}!
""" + help_text

my_account = """
👤<b>Моя учётная запись</b>
📝<b>Кол-во:</b> {signup_count}
"""

my_signups = """
👤<b>Мои записи</b>
📝<b>Кол-во:</b> {signup_count}
"""

register_create = '🤖Создаю новую учётную запись ...'

register_not = """
🤖Вы не зарегистрированные ...
🔧Пожалуйста, пройдите регистрацию: /register
"""

register_success = 'Привет {username}, вы теперь зарегистрированы!'

register_already = 'Привет {username}, вы уже зарегистрированы!'

register_fail = """
🤖Произошёл сбой при создании учётной записи ...
🔧Свяжитесь с поддержкой
"""

inline_fail = """
🤖Просим прощения, бот где-то поломался, но не сильно ...
🔧Начните заново: /start
"""

inline_expired = """
🤖Просим прощения, но данное собщение болье не действительно ...
🔧Начните заново: /start
"""

inline_expired_destroy = inline_expired + """
🗑️<i>Данное сообщение удалится через {seconds} секунд.</i>
<i>Подождите</i>
"""

events_page_body = """
<b>Страница:</b> {page_current} из {pages_total}
<b>Занятий: {elements_total}</b>
"""

events_page_detail = """
<b>{index}</b> - <i>{name}</i>
{start} - {end}
"""

signups_page_detail = """
<b>{index}</b> - <i>{name}</i>
{start} - {end}
"""

signup_success = """
Успешная запись!

📝<b>{name}</b>
{start} - {end}

Вы будете уведомлены до начала занятий
Нажмите /me чтобы просмотреть все ваши записи 
"""

signup_cancel = """
Запись удалена:

❌<b>{name}</b>
{start} - {end}
"""

event_detail = """
<i>{name}</i>
{start} - {end}
"""

signup_detail = """
<i>{name}</i>
{start} - {end}
"""
