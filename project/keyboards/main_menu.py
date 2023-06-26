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


#
# # Main menu buttons
# inline_btn_find_by_id = InlineKeyboardButton(
#     text="CVE по Id",
#     callback_data="find_cve_by_id"
# )
#
# inline_btn_most_valuable_cve = InlineKeyboardButton(
#     text="Значимые CVE",
#     callback_data="valuable_cve"
# )
#
# inline_btn_find_cve_web = InlineKeyboardButton(
#     text="CVE по параметрам (web)",
#     callback_data="find_cve_web"
# )
#
# inline_btn_find_cve_tg = InlineKeyboardButton(
#     text="CVE по параметрам",
#     callback_data="find_cve_tg"
# )
#
# inline_btn_find_poc_by_keywords = InlineKeyboardButton(
#     text="Поиск POC по ключевым словам",
#     callback_data="pocs_by_keywords"
# )
#
# inline_btn_subscribe_on_news = InlineKeyboardButton(
#     text="Подписка на новости выхода CVE",
#     callback_data="subscribe_on_news"
# )
#
# main_markup = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [inline_btn_find_by_id],
#         [inline_btn_find_cve_tg],
#         [inline_btn_most_valuable_cve],
#         [inline_btn_find_poc_by_keywords],
#     ]
# )
