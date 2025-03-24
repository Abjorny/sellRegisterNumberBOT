# -*- coding: utf-8 -*-
import logging
import asyncio
from aiogram import Bot, Dispatcher
from callbacks import peganator
from handlers import bot_message
import config
from forms import formRegisterProfile, formAddNumber, FormAddAdministrator,\
    FormEditNumber, FormSetPrice, FormSetActualTime, FormFoundMyNumber, \
    FormMassAddText, FormMassAddPhoto
    
from db import Database

DataBase = Database("DB.db")

logging.basicConfig(level=logging.INFO)

bot = Bot(token = config.TELEGRAM_BOT_TOKEN)

async def main():
    await DataBase.connect()
    dp = Dispatcher()
    
    dp.include_routers(
        peganator.router,
        formRegisterProfile.router,
        formAddNumber.router,
        FormAddAdministrator.router,
        FormEditNumber.router,
        FormSetPrice.router,
        FormSetActualTime.router,
        FormFoundMyNumber.router,
        FormMassAddText.router,
        FormMassAddPhoto.router,
        bot_message.router,
    )
    
    try:
        await dp.start_polling(bot)
    finally:
        await DataBase.close()
    
if __name__=='__main__':
    asyncio.run(main())