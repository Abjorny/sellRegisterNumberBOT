# -*- coding: utf-8 -*-
import logging
import asyncio
from aiogram import Bot, Dispatcher
from callbacks import peganator
from handlers import bot_message
import config
from forms import formRegisterProfile, formAddNumber, FormAddAdministrator, FormEditNumber
from db import Database

DataBase = Database("DB.db")

logging.basicConfig(level=logging.INFO)

bot = Bot(token = config.TELEGRAM_BOT_TOKEN)

async def main():
    await DataBase.connect()
    dp = Dispatcher()
    
    dp.include_routers(
        bot_message.router,
        peganator.router,
        formRegisterProfile.router,
        formAddNumber.router,
        FormAddAdministrator.router,
        FormEditNumber.router
    )
    
    try:
        await dp.start_polling(bot)
    finally:
        await DataBase.close()
    
if __name__=='__main__':
    asyncio.run(main())