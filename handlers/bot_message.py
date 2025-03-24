from keyboards import  fabric
from aiogram import  Router
from aiogram.enums.parse_mode import ParseMode
from Serializers.SerializersDefauls import UserSerializer
from aiogram.fsm.context import  FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from utilis.utilis import FormatedText
from db import Database
from aiogram import F

dataBase = Database("DB.db")
router = Router()

@router.message(Command('start'))
async def send_welcome(message: Message):
    user = UserSerializer(
        message = message
    )


    role = await user.get_role()
    text = f"*Доброго дня {user.username}!\n" \
            "Выберите интересующий пункт меню.*"
            
    text = FormatedText.formatMarkdownV2(text)
    
    await message.answer(
        text =text,
        reply_markup = fabric.pagination(0,user.id,'menu',[role]),
        parse_mode=ParseMode.MARKDOWN_V2,

    )


@router.message(F.text)
async def search_number(message: Message,state: FSMContext):
    await message.delete()
    orders_list = await dataBase.search_orders(message.text)
    text = "*Нажмите на интересующие вас предложение!*"
    last = "menu"
    await state.update_data(
        page = 0,
        type_query = "search",
        serach = message.text
    )
    
    if len(orders_list) < 10:
        last = "max"
    text = FormatedText.formatMarkdownV2(text)    
    await message.answer(
        text =text,
        reply_markup = fabric.pagination(3,0,last,orders_list),
        parse_mode=ParseMode.MARKDOWN_V2,

    )
