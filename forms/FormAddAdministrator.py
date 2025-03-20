from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from aiogram import Router, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText

router = Router()
dataBase = Database("DB.db")

class FormAddAdministrator(StatesGroup):
    userid = State()
    
@router.message(FormAddAdministrator.userid)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()    
    data = await state.get_data()
    
    if message.text.isdigit():
        user = await dataBase.get_user_userid(userid = int(message.text))
        if user is None:
            text = "*Ошибка пользователь с таким userid не зарегестрирован в боте!\nУкажите userid telegram пользователя, которому хотите выдать права администратора*"
        else:
            text = "*Успешно!\nПрава админстратора выданы.*"
            await state.clear()
            await dataBase.set_user_data(
                userid = int(message.text),
                key = "role",
                value = "admin"
            )
    
    else:
        text = "*Ошибка вы ввели не число!\nУкажите userid telegram пользователя, которому хотите выдать права администратора*"
        
    text = FormatedText.formatMarkdownV2(text)
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'adminPanel',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )