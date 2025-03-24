
from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText


router = Router()
dataBase = Database("DB.db")

class FormFoundMyNumber(StatesGroup):
    query = State()

@router.message(FormFoundMyNumber.query, F.text)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()    
    data = await state.get_data()
    orders_list = await dataBase.search_orders_by_user(message.text, message.chat.id) 
    
    page = 1
    last = "profile"
    
    if len(orders_list) > 0:
        page = 17
        text = f"*Список ваших номеров, по запросу: {message.text}*"
        await state.clear()
        if len(orders_list) < 10: last = "max"
        await state.update_data(
            page = 0,
            type_query = "searchProfile",
            serach = message.text
        )
        
    else:
        text = "*Не найдено номера в вашем личном кабинете, введите другой запрос.*"
    
    text = FormatedText.formatMarkdownV2(text)
    
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            page,
            0,
            last,
            orders_list
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )