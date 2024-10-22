from aiogram import F, Router
from aiogram.types import Message
from keyboards.main_menu import menu_kb
import yaml
from services.services import make_kbs
from aiogram.types import ReplyKeyboardRemove
from database.users import game_users
from database.travels import travels
from database.locations import locations
from database.conection import connection
from aiogram.filters import Command
from services.services import is_admin, is_senior_moderator
from lexicon.lexicon import LEXICON


with open('handlers/text/text.yaml', 'r', encoding='utf-8') as file:
    text: str = yaml.safe_load(file)

router = Router()


in_play: bool = False


@router.message(Command('start_reg'))
async def process_start_game_message(message: Message):
    if is_admin(message.from_user.id) or is_senior_moderator(message.from_user.id):
        global in_play
        in_play = True
        await message.answer(LEXICON['start_reg'])
    else:
        await message.answer(LEXICON['other_message'])


@router.message(Command('end_reg'))
async def process_end_registration_of_game(message: Message):
    if is_admin(message.from_user.id) or is_senior_moderator(message.from_user.id):
        global in_play
        in_play = False
        await message.answer(text=LEXICON['end_reg'])
    else:
        await message.answer(text=LEXICON['other_message'])


@router.message(F.text)
async def process_quest(message: Message):

    if (in_play and game_users[str(message.from_user.id)]['payed'] and message.text == LEXICON['play_button']) or game_users[str(message.from_user.id)]['in_play']:
        if str(message.text) == LEXICON['play_button'] and game_users[str(message.from_user.id)]['payed'] and game_users[str(message.from_user.id)]['went'] == 1 and game_users[str(message.from_user.id)]['stage'] == 1:
            game_users[str(message.from_user.id)]['went'] = 1
            game_users[str(message.from_user.id)]['stage'] = 1
            game_users[str(message.from_user.id)]['in_play'] = True
            await message.answer(text=text[1][1]['text'], reply_markup=make_kbs(text[1][1]['buttons']))
            game_users[str(message.from_user.id)]['went'] += 1
            game_users[str(message.from_user.id)]['in_play'] = True

        elif not game_users[str(message.from_user.id)]['in_play'] and not game_users[str(message.from_user.id)]['payed']:
            await message.answer(text=LEXICON['no_game'])

        elif message.text == 'Подсказка' and text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] in ['Dialog', 'EndDialog']:
            if game_users[str(message.from_user.id)]['help'] >= 4:
                await message.answer(text='Голос в голове: *Я тебе большим не помогу*')
            else:
                try:
                    await message.answer(text=text[
                        travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                        game_users[str(message.from_user.id)]['went']]['helps'][game_users[str(message.from_user.id)]['help']])
                    game_users[str(message.from_user.id)]['help'] += 1
                except Exception:
                    await message.answer(text='У этого задания нет подсказки')

        elif message.text == text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                    game_users[str(message.from_user.id)]['went']]['answer']:
            game_users[str(message.from_user.id)]['help'] = 0
            if text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'EndDialog':
                game_users[str(message.from_user.id)]['went'] = 1
                game_users[str(message.from_user.id)]['stage'] += 1
                if text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Dialog' and game_users[str(message.from_user.id)]['payed']:
                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['text'], reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['buttons']))

                elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Location':
                    await message.answer_location(latitude=locations[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]]['latitude'],
                                                  longitude=locations[travels[game_users[str(message.from_user.id)]['team']][
                                                      game_users[str(message.from_user.id)]['stage'] - 1]]['longitude'],
                                                  reply_markup=make_kbs(text[travels[
                                                      game_users[str(message.from_user.id)]['team']][
                                                      game_users[str(message.from_user.id)]['stage'] - 1]][
                                                                            game_users[str(message.from_user.id)]['went']][
                                                                            'buttons']))

            else:
                game_users[str(message.from_user.id)]['went'] += 1

                if text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Name':
                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']][
                        'text'], reply_markup=ReplyKeyboardRemove())
                    game_users[str(message.from_user.id)]['went'] += 1

                elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Location':
                    await message.answer_location(latitude=locations[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]]['latitude'],
                                                  longitude=locations[travels[game_users[str(message.from_user.id)]['team']][
                                                      game_users[str(message.from_user.id)]['stage'] - 1]]['longitude'],
                                                  reply_markup=make_kbs(text[travels[
                                                      game_users[str(message.from_user.id)]['team']][
                                                      game_users[str(message.from_user.id)]['stage'] - 1]][
                                                                            game_users[str(message.from_user.id)]['went']][
                                                                            'buttons']))

                elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'End':
                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['text'], reply_markup=menu_kb)

                    try:
                        print(f'{message.from_user.id} - End Game')
                        with connection.cursor() as cursor:
                            edit_payed = f"UPDATE users SET payed = 0  WHERE id = {message.from_user.id};"
                            edit_in_play = f"UPDATE users SET in_play = 0  WHERE id = {message.from_user.id};"
                            cursor.execute(edit_payed)
                            connection.commit()
                            cursor.execute(edit_in_play)
                            connection.commit()

                        game_users[str(message.from_user.id)]['payed'] = False
                        game_users[str(message.from_user.id)]['in_play'] = False

                    except Exception as es:
                        await message.answer(text=f'Ошибка: {es}. Перешлите это сообщение в поддержку')

                elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Photo':
                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['text'],
                                         reply_markup=ReplyKeyboardRemove())
                elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'SimpleText':

                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['text'],
                                         reply_markup=ReplyKeyboardRemove())
                    game_users[str(message.from_user.id)]['went'] += 1
                else:
                    await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']][
                        'text'], reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][
                        game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']][
                                                           'buttons']))



        # Location
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'Location':
            await message.answer_location(latitude=locations[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                'latitude'],
                                          longitude=locations[travels[game_users[str(message.from_user.id)]['team']][
                                              game_users[str(message.from_user.id)]['stage'] - 1]]['longitude'],
                                          reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][
                                              game_users[str(message.from_user.id)]['stage'] - 1]][
                                                                    game_users[str(message.from_user.id)]['went']][
                                                                    'buttons']))
        # Dialog
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'Dialog' and game_users[str(message.from_user.id)][
            'payed']:
            await message.answer(text=text[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][
                                     game_users[str(message.from_user.id)]['stage'] - 1]][
                                                           game_users[str(message.from_user.id)]['went']]['buttons']))
        # Name
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'Name':
            await message.answer(text=text[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=ReplyKeyboardRemove())
            game_users[str(message.from_user.id)]['went'] += 1
        # EnterName
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'EnterName':
            game_users[str(message.from_user.id)]['name'] = message.text
            game_users[str(message.from_user.id)]['went'] += 1
            await message.answer(text=text[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][
                                     game_users[str(message.from_user.id)]['stage'] - 1]][
                                                           game_users[str(message.from_user.id)]['went']]['buttons']))
        # EndDialog
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'EndDialog':
            await message.answer(text=text[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][
                                     game_users[str(message.from_user.id)]['stage'] - 1]][
                                                           game_users[str(message.from_user.id)]['went']]['buttons']))
        # EndDialog
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'EndDialog' and \
                text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                    game_users[str(message.from_user.id)]['went']]['answer'] == message.text:
            game_users[str(message.from_user.id)]['went'] = 1
            game_users[str(message.from_user.id)]['stage'] += 1
        # End
        elif text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
            game_users[str(message.from_user.id)]['went']]['class'] == 'End':
            await message.answer(text=text[
                travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][
                game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=menu_kb)

            try:
                print(f'{message.from_user.id} - End Game')
                with connection.cursor() as cursor:
                    edit_payed = f"UPDATE users SET payed = 0  WHERE id = {message.from_user.id};"
                    edit_in_play = f"UPDATE users SET in_play = 0  WHERE id = {message.from_user.id};"
                    cursor.execute(edit_payed)
                    connection.commit()
                    cursor.execute(edit_in_play)
                    connection.commit()

                game_users[str(message.from_user.id)]['payed'] = False
                game_users[str(message.from_user.id)]['in_play'] = False

            except Exception as es:
                await message.answer(text=f'Ошибка: {es}. Перешлите это сообщение в поддержку')

    elif message.text != LEXICON['play_button']:
        await message.answer(text=LEXICON['other_message'])

    else:
        await message.answer(text=LEXICON['no_game'])


@router.message(F.photo)
async def process_photo(message: Message):
    print(message.from_user.id)
    if game_users[str(message.from_user.id)]['in_play']:
        if text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['class'] == 'Photo':
            game_users[str(message.from_user.id)]['went'] += 1
            await message.answer(text=text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['text'],
                                 reply_markup=make_kbs(text[travels[game_users[str(message.from_user.id)]['team']][game_users[str(message.from_user.id)]['stage'] - 1]][game_users[str(message.from_user.id)]['went']]['buttons']))
    else:
        await message.answer(text=LEXICON['other_message'])