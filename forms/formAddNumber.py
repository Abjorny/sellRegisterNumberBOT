from aiogram.fsm.state import  State,StatesGroup
from API.SenderMessage import Notifications
from aiogram.fsm.context import  FSMContext
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText
from utilis.BasicFunctions import Order
from datetime import datetime


router = Router()
dataBase = Database("DB.db")

class FormAddNumber(StatesGroup):
    number = State()
    price = State()
    comment = State()
    photo = State()
    
@router.message(FormAddNumber.price, F.text)
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

@router.message(FormAddNumber.number, F.text)
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
    
    
@router.message(FormAddNumber.comment, F.text)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    await state.set_state(FormAddNumber.photo)
    await state.update_data(coment = message.text)
    data = await state.get_data()
    text = "*Успешно!\nОтправьте теперь фото, или нажмите кнопку пропустить.*"
    text = FormatedText.formatMarkdownV2(text)
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            14,
            message.from_user.id,
            'profile',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )

@router.message(FormAddNumber.photo, F.photo)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    data = await state.get_data()
    photos = data.get('photos', [])
    photos.append(message.photo[0].file_id)
    await state.update_data(photos = photos)
    text = f"*Успешно!\nОтправьте еще фото или нажмите кнопку 'Готово'\nСейчас фото = {len(photos)}\nМаксимум = 5*"
    
    if len(photos) >= 5:
        await state.clear()
        text = "*Успешно!\nВаш товар отправлен на расмотренние администратором.*"
        photos_str = await Order.format_photos_str(photos)
        ids = await Order.add_object(data, photos_str, message)
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
        
        
    text = FormatedText.formatMarkdownV2(text)
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            16,
            message.from_user.id,
            'profile',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )