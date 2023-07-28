from aiogram import types, Dispatcher
import sqlite3
from keyboard import menu, profile_menu, area_menu, backto_menu
from aiogram.dispatcher import FSMContext



class States:
    CHOOSE_CATEGORY = "choose_category"
    CHOOSE_TERRITORY = "choose_territory"



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



async def start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.username
    add_user_to_db(user_id)
    await message.answer("Добро пожаловать!\nВыберите категорию!", reply_markup=menu)


async def show_profile(message: types.Message):
    user_id = message.from_user.username
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Fetch the bonus score for the user
    cursor.execute("SELECT bonus_score FROM users WHERE telegram_username = ?", (user_id,))
    bonus_score = cursor.fetchone()[0]

    conn.close()

    # Send the profile message with the bonus score
    profile_message = f"Ваш баланс: {bonus_score}\nПриглашайте друзей в наше приложение и получайте бонусы!"
    await message.answer(profile_message, reply_markup=profile_menu)



async def back_to_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Меню", reply_markup=menu)




async def choose_category(message: types.Message, state: FSMContext):
    if await state.get_state() == States.CHOOSE_TERRITORY:
        await message.answer('Пожалуйста, выберите район из меню', reply_markup=area_menu)
        return

        # Save the chosen category in the user's state
    category = message.text
    await state.update_data(category=category)
    await state.set_state(States.CHOOSE_TERRITORY)  # Set the state to CHOOSE_TERRITORY
    await message.answer(f"Вы выбрали категорию: {category}", reply_markup=area_menu)


async def choose_area(message: types.Message, state: FSMContext):
    data = await state.get_data()
    category = data.get("category")

    # Check if a category was already chosen
    if category:
        chosen_area = message.text
        await state.finish()  # Finish the state
        await message.answer(f"Вы выбрали категорию: {category}\nТерриторию: {chosen_area}", reply_markup=backto_menu)
    else:
        await back_to_menu(message, state)



async def handle_invalid_input(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == States.CHOOSE_CATEGORY:
        await message.answer("Извините, я вас не понял.\nПожалуйста, выберите категорию из меню.", reply_markup=menu)
    elif current_state == States.CHOOSE_TERRITORY:
        await message.answer("Извините, я вас не понял.\nПожалуйста, выберите район из меню.", reply_markup=area_menu)
    else:
        await message.answer("Извините, я вас не понял.\nПожалуйста, выберите пункт из меню.", reply_markup=backto_menu)



def reg(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], state="*")
    dp.register_message_handler(show_profile, lambda message: message.text == "Профиль", state="*")
    dp.register_message_handler(back_to_menu, lambda message: message.text == "Вернуться в меню", state="*")
    dp.register_message_handler(choose_category,
                                lambda message: message.text in [
                                    "Рестораны",
                                    "Клубы",
                                    "Бары",
                                    "Экскурсии",
                                    "Развлечения",
                                    "Анонсы"
                                ],
                                state='*')
    dp.register_message_handler(choose_area,
                                lambda message: message.text in [
                                    "Сочи центральное",
                                    "Адлер",
                                    "Красная поляна"
                                ], state=States.CHOOSE_TERRITORY)
    dp.register_message_handler(handle_invalid_input, state="*")
