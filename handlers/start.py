from aiogram import types, Dispatcher
import sqlite3
from keyboard import menu, profile_menu

def add_user_to_db(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (id INTEGER PRIMARY KEY, 
                      telegram_username TEXT UNIQUE, 
                      bonus_score INTEGER)''')

    try:
        cursor.execute("INSERT INTO users (telegram_username, bonus_score) VALUES (?, ?)", (user_id, 0))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()



async def start(message: types.Message):
    user_id = message.from_user.username
    add_user_to_db(user_id)
    await message.answer("Добро пожаловать!", reply_markup=menu)



async def show_profile(query: types.CallbackQuery):
    user_id = query.from_user.username
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT bonus_score FROM users WHERE telegram_username=?", (user_id,))
    result = cursor.fetchone()
    bonus_score = result[0] if result else 0

    conn.close()

    await query.answer()
    await query.message.answer(
        f"Ваш баланс: {bonus_score}\nПриглашайте друзей в наше приложение и получайте бонусы!",
        reply_markup=profile_menu
    )



async def show_menu(query: types.CallbackQuery):
    await query.message.answer("Меню", reply_markup=menu)



async def process_inline_buttons(query: types.CallbackQuery):
    if query.data == "profile":
        await show_profile(query)
    elif query.data == "referral_link":
        await query.answer("Скопировано")
    elif query.data == "back":
        await show_menu(query)



def reg(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(process_inline_buttons)
