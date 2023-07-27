from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



restaurants_button = KeyboardButton("Рестораны", callback_data="restaurants")
clubs_button = KeyboardButton("Клубы", callback_data="clubs")
bars_button = KeyboardButton("Бары", callback_data="bars")
excursions_button = KeyboardButton("Экскурсии", callback_data="excursions")
entertainment_button = KeyboardButton("Развлечения", callback_data="entertainment")
events_button = KeyboardButton("Анонсы", callback_data="events")
profile_button = KeyboardButton("Профиль", callback_data="profile")

menu_buttons = [
    restaurants_button,
    clubs_button,
    bars_button,
    excursions_button,
    entertainment_button,
    events_button,
    profile_button,
]
menu = ReplyKeyboardMarkup(row_width=2)
menu.add(*menu_buttons)




ref_button = KeyboardButton("Реферальная ссылка", callback_data="referral_link")
back_button = KeyboardButton("Вернуться в меню", callback_data="back")

profile_buttons = [
    KeyboardButton("Реферальная ссылка", callback_data="referral_link"),
    KeyboardButton("Вернуться в меню", callback_data="back")
]
profile_menu = ReplyKeyboardMarkup(row_width=1)
profile_menu.add(*profile_buttons)




sochi_button = KeyboardButton("Сочи центральное", callback_data="sochi")
adler_button = KeyboardButton("Адлер", callback_data="adler")
red_glare_button = KeyboardButton("Красная поляна", callback_data="red_glade")

area_buttons = [
    sochi_button,
    adler_button,
    red_glare_button,
    back_button,
]
area_menu = ReplyKeyboardMarkup(row_width=1)
area_menu.add(*area_buttons)



backto_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(back_button)
