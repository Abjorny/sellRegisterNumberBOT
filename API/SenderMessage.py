from aiogram import types
from db import Database
from keyboards import fabric
dataBase = Database("DB.db")


class Notifications:
    @staticmethod
    async def send_notifs(
        text, page, data, last, users, message:types.Message
    ):
        for user in users:
            await message.bot.send_message(
                chat_id = user[1],
                text  = text,
                reply_markup=fabric.pagination(
                    page,
                    message.from_user.id,
                    last,
                    data
                ),
            )

    @staticmethod
    async def send_all_admins(
        text, page, data, last, message:types.Message
    ):
        admins = await dataBase.get_admins()
        await Notifications.send_notifs(
            text,page,data,last,admins, message
        )
