from vk_api.keyboard import VkKeyboard, VkKeyboardColor



# Создаем клавиатуры
def create_start_keyboard():
    
    keyboard_start = VkKeyboard(one_time=True)

    # Добавляем кнопки
    keyboard_start.add_button('Хочу разместить вакансию', color=VkKeyboardColor.POSITIVE)
    keyboard_start.add_button('Ищу работу', color=VkKeyboardColor.POSITIVE)

    return keyboard_start.get_keyboard()

def create_employerandadmin_keyboard():

    keyboard = VkKeyboard()

    keyboard.add_button('Правила размещения', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Реквизиты', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)
    return keyboard.get_keyboard()

def create_employer_keyboard():
    
    keyboard_employer = VkKeyboard()

    # Добавляем кнопки
    keyboard_employer.add_button('Позвать администратора', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Правила размещения', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Реквизиты', color=VkKeyboardColor.POSITIVE)
    keyboard_employer.add_line()
    keyboard_employer.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)

    return keyboard_employer.get_keyboard()

def create_applicant_keyboard(keywords):
    
    keyboard_applicant = VkKeyboard(one_time=True)
    
    if keywords:
        button_text = 'Редактировать ключевые слова'
    else:
        button_text = 'Добавить ключевые слова'

    # Добавляем кнопки
    keyboard_applicant.add_button(f'{button_text}', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    if keywords:
        keyboard_applicant.add_button('Просмотреть ключевые слова', color=VkKeyboardColor.POSITIVE)
        keyboard_applicant.add_line()
    keyboard_applicant.add_button('Пример слов', color=VkKeyboardColor.POSITIVE)
    keyboard_applicant.add_line()
    keyboard_applicant.add_button('Главное меню', color=VkKeyboardColor.POSITIVE)
    if keywords:
        keyboard_applicant.add_line()
        keyboard_applicant.add_button('Отменить подписку', color=VkKeyboardColor.NEGATIVE)

    return keyboard_applicant.get_keyboard()