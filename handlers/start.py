from aiogram import types, Dispatcher
import sqlite3

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
        # The user is already in the database (username is unique), so we catch the error and ignore it
        pass

    conn.commit()
    conn.close()

async def start(message: types.Message):

    user_id = message.from_user.username

    # Add the user to the database
    add_user_to_db(user_id)

    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Рестораны", callback_data="restaurants"),
        types.InlineKeyboardButton("Клубы", callback_data="clubs"),
        types.InlineKeyboardButton("Бары", callback_data="bars"),
        types.InlineKeyboardButton("Экскурсии", callback_data="excursions"),
        types.InlineKeyboardButton("Развлечения", callback_data="entertainment"),
        types.InlineKeyboardButton("Анонсы", callback_data="events"),
        types.InlineKeyboardButton("Профиль", callback_data="profile")
    ]
    markup.add(*buttons)
    await message.answer("Добро пожаловать!", reply_markup=markup)


async def show_profile(query: types.CallbackQuery):
    user_id = query.from_user.username
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Fetching the bonus_score for the user
    cursor.execute("SELECT bonus_score FROM users WHERE telegram_username=?", (user_id,))
    result = cursor.fetchone()
    bonus_score = result[0] if result else 0

    conn.close()

    # Inline keyboard for profile options
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("Реферальная ссылка", callback_data="referral_link"),
        types.InlineKeyboardButton("Вернуться назад", callback_data="back")
    )

    # Responding to the query with the user's profile and inline buttons
    await query.answer()
    await query.message.answer(
        f"Ваш баланс: {bonus_score}\nПриглашайте друзей в наше приложение и получайте бонусы!",
        reply_markup=markup
    )

async def process_inline_buttons(query: types.CallbackQuery):
    # Handling different inline button callbacks
    if query.data == "profile":
        await show_profile(query)
    elif query.data == "referral_link":
        await query.answer("Здесь будет ваша реферальная ссылка")
    elif query.data == "back":
        await query.answer("Вы вернулись назад")



def reg(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_callback_query_handler(process_inline_buttons)
