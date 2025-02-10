from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from aiogram import Router, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText
from API.SenderMessage import Notifications

router = Router()
dataBase = Database("DB.db")

class FormEditNumber(StatesGroup):
    value = State()

@router.message(FormEditNumber.value)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()    
    data = await state.get_data()
    text = "*Успешно!\nИнформация отредактирована и отправлена на модерацию.*"
    text = FormatedText.formatMarkdownV2(text)
    await dataBase.set_order_data(
        ids = data['thisOrderId'],
        key = data['typeEditValue'],
        value = message.text
    )
    await dataBase.set_order_data(
        ids = data['thisOrderId'],
        key = "status",
        value = "moderation"
    )
    order = await dataBase.get_order_id(data['thisOrderId'])
    admin_text = f"Новая заявка:\n\nАйди = {order[0]}\nНомер = {order[2]}\nКоменнтарий = {order[3]}\nЦена = {order[4]}\nСтатус = {order[6]}"    
    await Notifications.send_all_admins(
            text = admin_text,
            page = 9,
            data = [order[0]],
            last = "menu",
            message = message,
        )
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'getOrder',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )