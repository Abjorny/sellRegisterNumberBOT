from aiogram.fsm.state import  State,StatesGroup
from aiogram.fsm.context import  FSMContext
from utilis.BasicFunctions import Order
from aiogram import Router, F, types
from main import Bot
from keyboards import fabric
from db import Database
from utilis.utilis import FormatedText
from API.SenderMessage import Notifications
import zipfile
import tempfile
import os
from aiogram import types
from aiogram.fsm.context import FSMContext
from io import BytesIO


router = Router()
dataBase = Database("DB.db")

class FormMassAddPhoto(StatesGroup):
    archive = State()



@router.message(FormMassAddPhoto.archive, F.document)
async def send_welcome(message: types.Message, state: FSMContext, bot: Bot):
    await message.delete()
    dataState = await state.get_data()
    file_info = await bot.get_file(message.document.file_id)
    
    
    file_path = file_info.file_path
    count = 0
    temp_file_path = None
    
    try:
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            await bot.download_file(file_path, temp_file.name)
            temp_file_path = temp_file.name  

        if zipfile.is_zipfile(temp_file_path):
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                folder_structure = {}
                for file_name in zip_ref.namelist():
                    parts = file_name.split("/")
                    if len(parts) > 1:
                        folder = parts[0]
                        file = parts[-1]
                        if folder not in folder_structure:
                            folder_structure[folder] = []
                        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                            with zip_ref.open(file_name) as img_file:
                                img_data = img_file.read()
                                img_io = BytesIO(img_data)
                                input_file = types.BufferedInputFile(img_io.getvalue(), filename=file)
                                uploaded_photo = await bot.send_photo(
                                    message.chat.id, input_file, caption=f"Загружено из архива: {file_name}"
                                )
                                folder_structure[folder].append(uploaded_photo.photo[-1].file_id)
                                img_io.close()

                for folder, file_ids in folder_structure.items():
                    try:
                        data = folder.split("|")
                        dataObject = {
                            'number' : data[0].strip(),
                            'coment' : data[1].strip(),
                            'price' : data[2].strip(),
                        }
                        photos_str = await Order.format_photos_str(file_ids[:6])
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
                            fileid = file_ids
                        )
                        count +=1
                    except Exception as e:
                        print(e)
        
        text = f"*Успешно!\nВаши товары ( {count} штук ) отправлены на расмотренние администратором.*"
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
    
    finally:
        if (temp_file_path):
            os.remove(temp_file_path)