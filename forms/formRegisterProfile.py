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

class FormRegisterProfile(StatesGroup):
    email = State()
    number = State()

@router.message(FormRegisterProfile.email)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    await message.delete()
    await state.set_state(FormRegisterProfile.number)
    await state.update_data(email = message.text)
    
    data = await state.get_data()
    text = "*Успешно!\nТеперь укажите ваш номер телефона.*"
    text = FormatedText.formatMarkdownV2(text)
    
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'menu',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )
    
@router.message(FormRegisterProfile.number)
async def send_welcome(message : types.Message,state: FSMContext,bot:Bot):
    data = await state.get_data()
    await message.delete()
    await state.clear()    
    
    user = await dataBase.get_user_userid(message.from_user.id)
    role = user[4]
    
    if role == "moderation":
        text = "*У вас уже есть активная заявка на регистрацию, пожалуйста дождитесь ее решения.*"
    
    elif role in ['verif', 'admin']:
        text = f"*Вы уже прошли регестрацию, ваша текущая роль {role}*"
    
    else:
        text = "*Заяка на модерацию отправлена администраторам.*"
        await dataBase.set_user_data(
            userid = message.from_user.id,
            key = "email",
            value = data['email']
        )
        await dataBase.set_user_data(
            userid = message.from_user.id,
            key = "number",
            value = message.text
        )
        await dataBase.set_user_data(
            userid = message.from_user.id,
            key = "role",
            value = "moderation"
        )
        admin_text = f"Новая заяка!\n\nПервое имя = {message.from_user.first_name}\nВторое имя = {message.from_user.last_name}\nUserid = {message.from_user.id}\nEmail = {data['email']}\nНомер телефона = {message.text}"
        await Notifications.send_all_admins(
            text = admin_text,
            page = 2,
            data = [message.from_user.id],
            last = "menu",
            message = message
        )

    text = FormatedText.formatMarkdownV2(text)
    await bot.edit_message_text(
        text = text,
        reply_markup=fabric.pagination(
            1,
            message.from_user.id,
            'menu',
            []
        ),
        parse_mode='MarkdownV2',
        message_id=data['lastid'],
        chat_id=message.chat.id
    )
    
    