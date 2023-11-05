from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def edit_delay_keyboard(group):

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Дата"))
    keyboard.add(KeyboardButton("Время начала"))
    keyboard.add(KeyboardButton("Время завершения"))

    if group.parsers:
        keyboard.add(KeyboardButton("Изменить парсеры"))
        keyboard.add(KeyboardButton("Начать парсинг"))
    else:
        keyboard.add(KeyboardButton("Добавить парсеры"))

    if group.DEFAULT_POST_PHOTO:
        keyboard.add(KeyboardButton("Изменить фото для постов"))
    else:
        keyboard.add(KeyboardButton("Добавить фото по умолчанию (посты с тг выкладываются без фото)"))

    keyboard.add(KeyboardButton("Меню группы"))

    return keyboard

def editing_parsers_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Добавить парсер тг"))
    keyboard.add(KeyboardButton("Удалить парсер"))
    keyboard.add(KeyboardButton("Меню"))

    return keyboard

def delete_parser_keyboard(group):

    keyboard = ReplyKeyboardMarkup(row_width=1)

    for parser in group.parsers:

        keyboard.add(KeyboardButton(parser.resource))

    keyboard.add(KeyboardButton("Завершить"))

    return keyboard

def on_start_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Сделать отложку"))
    keyboard.add(KeyboardButton("Отменить изменения"))

    return keyboard

def choose_date_keyboard():

    keyboard = ReplyKeyboardMarkup(row_width=1)

    keyboard.add(KeyboardButton("Сегодня"))
    keyboard.add(KeyboardButton("Завтра"))

    return keyboard

def inline_keyboard(chat_id, message_id, post):

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton("Удалить", callback_data=f"remove_{chat_id}_{message_id}_{post.id}"))

    return keyboard

