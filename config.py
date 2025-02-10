from dotenv import load_dotenv
import os

os.environ.pop("TELEGRAM_BOT_TOKEN", None)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_KEY = os.getenv("CRYPTO_BOT_TOKEN")
start_menu = [
    {
        "title" : "⭐ Витрина номеров",
        "action" : "ordersList"
    },
]

profile_menu = [
    {
        "title" : "Подтвердить актуальность",
        "action" : "acceptActual"
    },
    {
        "title" : "Мои номера",
        "action" : "listNumbers"
    },
    {
        "title" : "Добавить номер",
        "action" : "addNumber"
    },
    {
        "title" : "Удалить номер",
        "action" : "deleateNumber"
    },
]

admin_menulist = [
    {
        "title" : "Заявки модерации",
        "action" : "listModerations"
    },
    {
        "title" : "Добавить администратора",
        "action" : "addAdministrator"
    },
    {
        "title" : "Удалить администратора",
        "action" : "deleateAdministrator"
    },
    {
        "title" : "Установить цену",
        "action" : "setPrice"
    },
]
profile_button = {
    "title" : "💼 Профиль",
    "action" : "profile"
}

adminPanel_button = {
    "title" : "👑 Админ панель",
    "action" : "adminPanel"
}
register_button = {
    "title" : "📝 Регистрация",
    "action" : "registerProfile"
}

admin_menu, verif_menu = start_menu.copy(), start_menu.copy()

start_menu.append(
    register_button
)
verif_menu.append(
    profile_button
)

admin_menu.append(
    adminPanel_button
)
admin_menu.append(
    profile_button
)

