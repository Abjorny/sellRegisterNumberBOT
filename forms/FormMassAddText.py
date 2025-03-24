from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from utilis.BasicFunctions import Order
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText
from API.SenderMessage import Notifications


router = Router()
dataBase = Database("DB.db")

class FormMassAddText(StatesGroup):
    text = State()

@router.message(FormMassAddText.text, F.text)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()    
    dataState = await state.get_data()
    await state.clear()
    orders = message.text.split("\n")
    photos = dataState.get('photos', None)

    for order in orders:
        try:
            data = order.split("|")
            dataObject = {
                'number' : data[0].strip(),
                'coment' : data[1].strip(),
                'price' : data[2].strip(),
            }
            photos_str = await Order.format_photos_str(photos)
            ids = await Order.add_object(dataObject, photos_str, message)
            await Order.update_actual_time(message)
            order = await dataBase.get_order_id(ids)
            admin_text = await Order.admin_text_add(order, message)
            await Notifications.send_all_admins(
                text = admin_text,
                page = 9,
                data = [ids],
                last = "menu",
                message = message,
                fileid = photos
            )
        except Exception as e:
            print(e)
        
    text = f"*Успешно!\nВаши товары ( {len(orders)} штук ) отправлены на расмотренние администратором.*"
    text = FormatedText.formatMarkdownV2(text)
    
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            0,
            "profile",
            []
        ),
        parse_mode='MarkdownV2',
        message_id=dataState['lastid'],
        chat_id=message.chat.id
    )