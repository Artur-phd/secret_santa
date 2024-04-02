from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import time
import sqlite3
from configurate import functions, classes, settings
from configurate.languages import lang
import time 


bot = Bot(settings.__TOKEN, parse_mode='html')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

functions.db_connect(db_name="players_data.sql", request="CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, user_id varchar(30), name_user TEXT, level INT, team TEXT, recipient TEXT, wishes TEXT, status_game varchar(10), game_rools TEXT)", do='post')
functions.db_connect(db_name="players_data.sql", request="CREATE TABLE IF NOT EXISTS levels (id varchar(30), level INT)", do='post')


class RechangeTeam(StatesGroup):
    new_team = State()

class MessageRecipient(StatesGroup):
    message_text = State()

class User(StatesGroup):
    user_name = State()
    team_name = State()
    wishes = State()




@dp.message_handler(commands=['menu'])
async def menu(message: types.Message):
    if functions.check_user(message.from_user.id) is True:
        markup = types.InlineKeyboardMarkup(row_width=2)
        profil = types.InlineKeyboardButton('Profil', callback_data='profil')
        team = types.InlineKeyboardButton('Team', callback_data='team')
        start_game = types.InlineKeyboardButton('Start', callback_data='start_game')
        see_profil = types.InlineKeyboardButton("see the recipient's profile", callback_data='see_profil')
        send_message_elf =  types.InlineKeyboardButton("send message recipient's", callback_data='send_message')
        markup.add(profil, team, see_profil, send_message_elf, start_game)
        await message.answer("<b>MENU</b>", reply_markup=markup)   
    else:
        await message.answer("Вам нужно зарегистрироваться!")
        await User.user_name.set()
        await message.answer("Напишите своё имя!")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if functions.check_user(message.from_user.id) is True:
        await message.answer("Добро пожаловать! Нажми на /menu")

    else:
        await message.answer("Вам нужно зарегистрироваться!")
        await User.user_name.set()
        await message.answer("Напишите своё имя!")


@dp.message_handler(state=User.user_name)
async def user_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['user_name'] = message.text
        if functions.check_name(message.text) is True:
            await User.next()
            await message.answer("Отлично! Придумай имя для своей команды.")         
        else:
            await message.answer('Это имя занято - введите другое!')


@dp.message_handler(state=User.wishes)
async def user_wishes(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['wishes'] = message.text
        await message.answer("Super!")

        markup = types.InlineKeyboardMarkup(row_width=2)
        save = types.InlineKeyboardButton('Save', callback_data='save')
        edit = types.InlineKeyboardButton('Edit', callback_data='edit')
        markup.add(save, edit)
        await User.next()
        await message.answer(f"<i>Вот твой профиль:</i> \n<b>Имя:</b> <i>{data['user_name']}</i>\n<b>Команда:</b><i>{data['team_name']}</i>\n<b>получатель</b>: <i>не найден</i>\n<b>Пожелания к подарку</b> <i>{data['wishes']}</i>", reply_markup=markup)
        

@dp.message_handler(state=MessageRecipient.message_text)
async def message_sent(message: types.Message, state=FSMContext):
    conn = sqlite3.connect("players_data.sql")
    cur = conn.cursor()

    cur.execute("SELECT name_user FROM users WHERE user_id = '%s' " % (message.from_user.id))
    data1 = cur.fetchall()
    cur.execute("SELECT user_id FROM users WHERE recipient = '%s' " % (data1[0][0]))
    result_data = cur.fetchall()
    conn.close()
    await MessageRecipient.next()

    await message.bot.send_message(result_data[0][0], f'<i>Тебе пришо сообщение от санты!🎅🏼</i>\n\n<b>"{message.text}"</b>')
    await message.answer('Message sent!')



@dp.message_handler(state=User.team_name)
async def team_name(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        if functions.check_team(message.text) is True:
            data['team_name'] = message.text
            await User.next()
            await message.answer("Тепрь введи свои пожелания к подарку!")
        else:
            await message.answer('В этой команде уже проходит игра - введи другую!')
        


@dp.message_handler(state=RechangeTeam.new_team)
async def new_team(message: types.Message, state=FSMContext):
    functions.db_connect(db_name='players_data.sql', request="UPDATE users SET team = '%s' WHERE user_id = '%s'" % (message.text, message.from_user.id), do='post')
    await RechangeTeam.next()
    await message.answer('Готово - заходи в профиль!')



@dp.callback_query_handler()
async def call_qh(call: types.CallbackQuery, state=FSMContext):


    # CREATE PROFIL
    if call.data == 'save':
        async with state.proxy() as data:
            ad = classes.CreateProfil()
            ad.add_in_db(user_id=call.message.chat.id, name=data['user_name'], team_name=data['team_name'], wishes=data['wishes'], status='Off')
            await call.message.edit_text('/menu')
    elif call.data == 'edit':
        functions.db_connect(db_name="players_data.sql", request="DELETE FROM users WHERE user_id = '%s'" % (call.from_user.id), do='post')
        await call.message.edit_text('Ok')
        await User.user_name.set()
        time.sleep(0.3)
        await call.message.edit_text('Введи своё имя!')
        


        

    #MENU BUTTONS
    elif call.data == 'profil' and functions.check_user(call.from_user.id) is True:
        user_data = functions.db_connect(db_name='players_data.sql', request="SELECT * FROM users WHERE user_id = '%s'" % (call.from_user.id), do='get')
        markup = types.InlineKeyboardMarkup(row_width=1)
        team = types.InlineKeyboardButton('Team', callback_data='team')
        start_game = types.InlineKeyboardButton('Start', callback_data='start_game')
        see_profil = types.InlineKeyboardButton("see the recipient's profile", callback_data='see_profil')
        send_message_elf =  types.InlineKeyboardButton("send message recipient's", callback_data='send_message')
        if functions.check_status_game(call.from_user.id) is True:
            markup.add(types.InlineKeyboardButton('Edit profil', callback_data='edit'))
        elif functions.check_status_game(call.from_user.id) is False:
            markup.add(types.InlineKeyboardButton('end the game', callback_data='game_overs'))
        markup.add(team, see_profil, send_message_elf, start_game)
        await call.message.edit_text(text=f"⛄️Имя: {user_data[0][2]}\n 📈Уровень: {user_data[0][3]}\n👨‍👩‍👧‍👧Команда: {user_data[0][4]}\n👹Получатель: ✨{user_data[0][5]}✨\n😉Пожелания: {user_data[0][6]}\n", reply_markup=markup)
    elif call.data == 'team' and functions.check_user(call.from_user.id) is True:
        conn = sqlite3.connect('players_data.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = '%s'" % (call.from_user.id))
        user_data_1 = cur.fetchall()
        cur.execute("SELECT name_user FROM users WHERE team = '%s'" % (user_data_1[0][4]))
        user_data_2 = cur.fetchall()
        conn.close()
        team_data = ''
        for name in user_data_2:
            team_data += f'⛄️{name[0]}\n'
        markup = types.InlineKeyboardMarkup(row_width=1)
        profil = types.InlineKeyboardButton('Profil', callback_data='profil')
        start_game = types.InlineKeyboardButton('Start', callback_data='start_game')
        see_profil = types.InlineKeyboardButton("see the recipient's profile", callback_data='see_profil')
        send_message_elf =  types.InlineKeyboardButton("send message recipient's", callback_data='send_message')
        markup.add(profil, see_profil, send_message_elf, start_game)    
        await call.message.edit_text(text=str(team_data), reply_markup=markup)
    elif call.data == 'start_game' and functions.tren(call.from_user.id) % 2 == 1 and functions.check_user(call.from_user.id) is True:
        await call.answer('Нечётное количество игроков')
    elif call.data == 'start_game' and functions.tren(call.from_user.id) % 2 == 0 and functions.check_status_game(call.from_user.id) is True and functions.check_user(call.from_user.id) is True:
        rools = functions.boom(functions.start_game_list(call.from_user.id))
        conn = sqlite3.connect('players_data.sql')
        cur = conn.cursor()
        cur.execute("SELECT name_user, team FROM users WHERE user_id = '%s'" % (call.from_user.id))
        user_name_team = cur.fetchall()
        rool = functions.rools_format_sql(rools)
        cur.execute("UPDATE users SET status_game = '%s' WHERE team = '%s'" % ('On', user_name_team[0][1]))
        cur.execute("UPDATE users SET game_rools = '%s' WHERE team = '%s'" % (rool, user_name_team[0][1]))
        conn.commit()
        conn.close()
        functions.start_play(team = user_name_team[0][1], rools=rools)
        id_players = functions.db_connect(db_name='players_data.sql', request="SELECT user_id FROM users WHERE team = '%s'" % (user_name_team[0][1]), do="get")
        for id_play in id_players:
            await call.message.bot.send_message(id_play[0], "Игра началась - проверяй свой профиль!")


        await call.message.edit_text(f'Ты даришь подарок игроку: <b>{rools[user_name_team[0][0]]}</b>')   

    elif call.data == 'start_game' and functions.tren(call.from_user.id) % 2 == 0 and functions.check_status_game(call.from_user.id) is False and functions.check_user(call.from_user.id) is True:
        await call.answer("посмотри в свой профиль!")  

    elif call.data == 'see_profil' and functions.check_status_game(call.from_user.id) is False and functions.check_user(call.from_user.id) is True:
        user_data_stock = functions.db_connect(db_name='players_data.sql', request="SELECT * FROM users WHERE user_id = '%s'" % (call.from_user.id), do='get')  
        user_data = functions.db_connect(db_name='players_data.sql', request="SELECT * FROM users WHERE name_user = '%s'" % (user_data_stock[0][5]), do='get')
        markup = types.InlineKeyboardMarkup(row_width=1)
        profil = types.InlineKeyboardButton('Profil', callback_data='profil')
        team = types.InlineKeyboardButton('Team', callback_data='team')
        start_game = types.InlineKeyboardButton('Start', callback_data='start_game')
        send_message_elf =  types.InlineKeyboardButton("send message recipient's", callback_data='send_message')
        markup.add(profil, team, send_message_elf, start_game)
        await call.message.edit_text(text=f"<b>Вот профиль получателя:\n\n</b>⛄️Имя: {user_data[0][2]}\n 📈Уровень: {user_data[0][3]}\n👨‍👩‍👧‍👧Команда: {user_data[0][4]}\n😉Пожелания: {user_data[0][6]}\n", reply_markup=markup)
    elif call.data == 'see_profil' and functions.check_status_game(call.from_user.id) is True and functions.check_user(call.from_user.id) is True:
        await call.answer('Вы ещё не начали игру!')
    elif call.data == 'send_message' and functions.check_status_game(call.from_user.id) is False and functions.check_user(call.from_user.id) is True:
        await MessageRecipient.message_text.set()
        await call.message.edit_text('Напиши сообщение, мы его отправим получателю твоего подарка😉')
    elif call.data == 'send_message' and functions.check_status_game(call.from_user.id) is True and functions.check_user(call.from_user.id) is True:
        await call.answer("Игра ещё не началась!")
    elif call.data == "game_overs":
        markup = types.InlineKeyboardMarkup(row_width=2)
        yes = types.InlineKeyboardButton('yes', callback_data='yes_end_game')
        no = types.InlineKeyboardButton('No', callback_data='no_end_game')
        markup.add(yes, no)

        await call.message.edit_text('Вы точно хотите завершить игру (команда будет распущена и вам нужно будет пересоздать профиль)?', reply_markup=markup)

    elif call.data == 'yes_end_game':
        team_data = functions.db_connect(db_name='players_data.sql', request="SELECT team FROM users WHERE user_id = '%s'" % (call.from_user.id), do='get')
        team_id = functions.db_connect(db_name='players_data.sql', request="SELECT user_id FROM users WHERE team = '%s'" % (team_data[0][0]), do='get')
        functions.db_connect(db_name='players_data.sql', request="DELETE FROM users WHERE user_id = '%s'" % (call.from_user.id), do='post')
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        new_game = types.InlineKeyboardButton('new game!', callback_data='new_game')
        markup.add(new_game)
        for user in team_id: 
            await call.message.bot.send_message(user[0], "Игра окончена!\n Удачи😉", reply_markup=markup)
    elif call.data == 'no_end_game':
        user_data = functions.db_connect(db_name='players_data.sql', request="SELECT * FROM users WHERE user_id = '%s'" % (call.from_user.id), do='get')
        markup = types.InlineKeyboardMarkup(row_width=1)
        team = types.InlineKeyboardButton('Team', callback_data='team')
        start_game = types.InlineKeyboardButton('Start', callback_data='start_game')
        see_profil = types.InlineKeyboardButton("see the recipient's profile", callback_data='see_profil')
        send_message_elf =  types.InlineKeyboardButton("send message recipient's", callback_data='send_message')
        if functions.check_status_game(call.from_user.id) is True:
            markup.add(types.InlineKeyboardButton('Edit profil', callback_data='edit'))
        elif functions.check_status_game(call.from_user.id) is False:
            markup.add(types.InlineKeyboardButton('end the game', callback_data='game_overs'))
        markup.add(team, see_profil, send_message_elf, start_game)
        await call.message.edit_text(text=f"⛄️Имя: {user_data[0][2]}\n 📈Уровень: {user_data[0][3]}\n👨‍👩‍👧‍👧Команда: {user_data[0][4]}\n👹Получатель: ✨{user_data[0][5]}✨\n😉Пожелания: {user_data[0][6]}\n", reply_markup=markup)
    elif call.data == 'new_game':
        lo = functions.db_connect(db_name='players_data.sql', request="SELECT level FROM levels WHERE id = '%s'" % (call.from_user.id), do='get')
        if len(lo) != 0: 
            level = int(lo[0][0])
            level += 1
            functions.db_connect(db_name='players_data.sql', request="UPDATE levels SET level = '%s' WHERE id = '%s'" % (level, call.from_user.id), do='post')        
        functions.db_connect(db_name="players_data.sql", request="DELETE FROM users WHERE user_id = '%s'" % (call.from_user.id), do='post')
        await call.message.edit_text('Ok')
        await User.user_name.set()
        time.sleep(0.3)
        await call.message.edit_text('Введи своё имя!')


executor.start_polling(dp)
