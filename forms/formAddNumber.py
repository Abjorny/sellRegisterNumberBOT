from aiogram.fsm.state import  State,StatesGroup
from API.SenderMessage import Notifications
from aiogram.fsm.context import  FSMContext
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText


router = Router()
dataBase = Database("DB.db")

class FormAddNumber(StatesGroup):
    number = State()
    price = State()
    comment = State()
    
@router.message(FormAddNumber.price)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    await state.set_state(FormAddNumber.comment)
    await state.update_data(price = message.text)
    
    data = await state.get_data()
    text = "*Успешно!\nВведите комментарий.*"
    text = FormatedText.formatMarkdownV2(text)
    
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'profile',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )

@router.message(FormAddNumber.comment)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    
    data = await state.get_data()
    text = "*Успешно!\nВаш товар отправлен на расмотренние администратором.*"
    text = FormatedText.formatMarkdownV2(text)
    url = f'https://t.me/{message.from_user.username}' if message.from_user.username != None and  message.from_user.username != '' \
        else message.from_user.url
    ids = await dataBase.add_order(
        userid = message.from_user.id,
        url =  url,
        number = data['number'],
        comment = message.text,
        price = data['price']
    )
    
    order = await dataBase.get_order_id(ids)
    
    admin_text = f"Новая заявка:\n\nАйди = {order[0]}\nИмя = {message.from_user.first_name}\nUserid = {order[1]}\nНомер = {order[2]}\nКоменнтарий = {order[3]}\nЦена = {order[4]}\nСтатус = {order[6]}"    
   
    await Notifications.send_all_admins(
        text = admin_text,
        page = 9,
        data = [ids],
        last = "menu",
        message = message
    )
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'profile',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )
    
    await state.clear()

@router.message(FormAddNumber.number)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    await state.set_state(FormAddNumber.price)
    await state.update_data(number = message.text)
    
    data = await state.get_data()
    text = "*Успешно!\nВведите цену.*"
    text = FormatedText.formatMarkdownV2(text)
    
    
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'profile',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )