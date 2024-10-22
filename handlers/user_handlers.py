from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, callback_query
from aiogram.types.callback_query import CallbackQuery
from keyboards.main_menu import access_send, other_commands_kb, back_kb, menu_kb, teams, team_kb, access_payment_kb
from lexicon.lexicon import LEXICON
from config_data.config import Config, load_config
from database.users import game_users
from database.conection import connection
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.services import is_admin, is_moderator, is_senior_moderator

config: Config = load_config()


router = Router()


class SendReport(StatesGroup):
    report = State()

# region Commands


@router.message(CommandStart())
async def process_start_command(message: Message):
    try:
        with connection.cursor() as cursor:
            add_player = f"INSERT INTO `users` (id, name, in_play, stage, went, team, help, payed, pre_team, role) VALUES ({message.from_user.id}, 'Gamer', false, 1, 1, 0, 0, false, 0, 1);"
            cursor.execute(add_player)
            connection.commit()

        game_users[str(message.from_user.id)] = {'name': 'Gamer', 'in_play': False, 'stage': 1, 'went': 1, 'team': 0, 'help': 0, 'payed': False, 'pre_team': 0, 'role': 1}

    except Exception:
        pass

    await message.answer(text=LEXICON['/start'], reply_markup=menu_kb)


@router.message(Command('help'))
async def process_help_message(message: Message):
    await message.answer(text=LEXICON['FAQ'], reply_markup=other_commands_kb)


@router.message(Command('report'))
async def process_report(message: Message, state: FSMContext):
    await message.answer('Напишите ваш репорт: ')
    await state.set_state(SendReport.report)
# endregion

# region Strings


@router.message(F.text == LEXICON['FAQ_button'])
async def process_faq(message: Message):
    await message.answer(text=LEXICON['FAQ'], reply_markup=other_commands_kb)


@router.message(F.text == LEXICON['sale_button'])
async def process_sale_ticket(message: Message):
    if game_users[str(message.from_user.id)]['in_play']:
        await message.answer(LEXICON['in_play'])
    else:
        if game_users[str(message.from_user.id)]['payed']:
            await message.answer(text=LEXICON['payed'])
        else:
            await message.answer(text=f'Выберите команду:', reply_markup=team_kb)

# endregion

# region Callbacks


@router.callback_query(F.data.startswith('team_'))
async def process_choose_team(call: CallbackQuery):
    if teams[int(call.data[5])] == 0:
        await call.message.answer(text=f'Команда {call.data[5]} заполнена. Выберите команду еще раз:', reply_markup=team_kb)
    else:
        try:
            with connection.cursor() as cursor:
                edit_pre_team = f"UPDATE `users` SET pre_team = '{int(call.data[5])}' WHERE id = {call.from_user.id};"
                cursor.execute(edit_pre_team)
                connection.commit()

            game_users[str(call.from_user.id)]['pre_team'] = int(call.data[5])
            await call.message.answer(text=f'Вы выбрали команду {call.data[5]}', reply_markup=access_payment_kb)

        except Exception as es:
            await call.message.answer(text=f'Ошибка: {es}. Пожалуйста перешлите это письмо в тех. поддержку')


@router.callback_query(F.data == 'moder_commands')
async def process_moder_commands(call: CallbackQuery):
    if game_users[str(call.from_user.id)]['in_play']:
        await call.message.answer(LEXICON['in_play'])
    else:
        if is_admin(call.from_user.id) or is_senior_moderator(call.from_user.id) or is_moderator(call.from_user.id):
            await call.message.edit_text(text=LEXICON['moder_commands'], reply_markup=back_kb)
        else:
            await call.answer(text='У вас недостаточно прав')


@router.callback_query(F.data == 'admin_commands')
async def process_moder_commands(call: CallbackQuery):
    if game_users[str(call.from_user.id)]['in_play']:
        await call.message.answer(LEXICON['in_play'])
    else:
        if is_admin(call.from_user.id) or is_senior_moderator(call.from_user.id):
            await call.message.edit_text(text=LEXICON['admin_commands'], reply_markup=back_kb)
        else:
            await call.answer(text='У вас недостаточно прав')


@router.callback_query(F.data == 'back')
async def process_back(call: CallbackQuery):
    if game_users[str(call.from_user.id)]['in_play']:
        await call.message.answer(LEXICON['in_play'])
    else:
        await call.message.edit_text(text=LEXICON['FAQ'], reply_markup=other_commands_kb)

# endregion

# region FSM


@router.message(F.text, SendReport.report)
async def process_send_report(message: Message, state: FSMContext):
    try:
        if len(message.text) <= 300:
            with connection.cursor() as cursor:
                add_report = f"INSERT INTO reports (user_id, text) VALUES ({message.from_user.id}, '{message.text}');"
                cursor.execute(add_report)
                connection.commit()

            await message.answer('Ваша жалоба отправлена')
            await state.clear()
        else:
            await message.answer('Текст жалобы до 300 символов')

    except Exception as es:
        await message.answer(text=f'Ошибка: {es}. Пожалуйста перешлите это письмо в тех. поддержку')

# endregion
