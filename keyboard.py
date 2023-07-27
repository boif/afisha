from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu_buttons = [
    InlineKeyboardButton("Рестораны", callback_data="restaurants"),
    InlineKeyboardButton("Клубы", callback_data="clubs"),
    InlineKeyboardButton("Бары", callback_data="bars"),
    InlineKeyboardButton("Экскурсии", callback_data="excursions"),
    InlineKeyboardButton("Развлечения", callback_data="entertainment"),
    InlineKeyboardButton("Анонсы", callback_data="events"),
    InlineKeyboardButton("Профиль", callback_data="profile")
]

menu = InlineKeyboardMarkup(row_width=2)
menu.add(*menu_buttons)

profile_buttons = [
    InlineKeyboardButton("Реферальная ссылка", callback_data="referral_link"),
    InlineKeyboardButton("Вернуться назад", callback_data="back")
]
profile_menu = InlineKeyboardMarkup(row_width=1)
profile_menu.add(*profile_buttons)
