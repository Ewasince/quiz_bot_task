from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Greetings menu buttons
inline_btn_menu = InlineKeyboardButton(
    text="Погнали",
    callback_data="menu_btn"
)

# markups 
start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [inline_btn_menu]
    ]
)