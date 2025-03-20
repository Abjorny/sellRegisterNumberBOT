from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText


router = Router()
dataBase = Database("DB.db")

class FormSetPrice(StatesGroup):
    price = State()

@router.message(FormSetPrice.price, F.text)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()    
    data = await state.get_data()
    if message.text.isdigit():

        text = f"*Успешно!\nНовая стоимость за подписку - {message.text}.*"
        await state.clear()
        await dataBase.set_settings_data(
            key = 'price',
            value = message.text
        )
    
    else:
        text = "*Ошибка вы ввели не число!\nУкажите новую стоимость в долларах за месяц ( просто число )*"
    
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