from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from database.teams import teams

from lexicon.lexicon import LEXICON

faq_kb_button = KeyboardButton(text=LEXICON['faq_button'])
sale_kb_button = KeyboardButton(text=LEXICON['sale_button'])
play_kb_button = KeyboardButton(text=LEXICON['play_button'])

menu_kb = ReplyKeyboardMarkup(
    keyboard=[[play_kb_button],
              [sale_kb_button],
              [faq_kb_button]],
    resize_keyboard=True
)

team_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=f'Команда 1: {teams[1]}', callback_data='team_1')],
                     [InlineKeyboardButton(text=f'Команда 2: {teams[2]}', callback_data='team_2')],
                     [InlineKeyboardButton(text=f'Команда 3: {teams[3]}', callback_data='team_3')],
                     [InlineKeyboardButton(text=f'Команда 4: {teams[4]}', callback_data='team_4')]]
)


role_for_admins_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Игрок', callback_data='role_1')],
                     [InlineKeyboardButton(text='Модератор', callback_data='role_2')],
                     [InlineKeyboardButton(text='Старший модератор', callback_data='role_3')],
                     [InlineKeyboardButton(text='В главное меню❌', callback_data='close_set_role')]]
)

role_for_senior_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Игрок', callback_data='role_1')],
                     [InlineKeyboardButton(text='Модератор', callback_data='role_2')],
                     [InlineKeyboardButton(text='В главное меню❌', callback_data='close_set_role')]]
)

close_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='В главное меню❌', callback_data='close_set_role')]]
)

access_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Подтвердить', callback_data='access_set_role')],
                     [InlineKeyboardButton(text='В главное меню❌', callback_data='close_set_role')]]
)

access_send = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Подтвердить', callback_data='access_send')],
                     [InlineKeyboardButton(text='Отказаться', callback_data='close_fill')]]
)

help_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Подсказка')]],
    resize_keyboard=True
)

other_commands_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Команды для модеров', callback_data='moder_commands')],
                     [InlineKeyboardButton(text='Команды для с. модеров и админов', callback_data='admin_commands')]]
)

back_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Назад', callback_data='back')]]
)

access_payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Подтвердить', callback_data='access_payment')]]
)
