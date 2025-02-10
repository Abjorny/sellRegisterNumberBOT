from keyboards import  fabric
from aiogram import  Router
from aiogram.enums.parse_mode import ParseMode
from Serializers.SerializersDefauls import UserSerializer
from aiogram.filters import Command
from aiogram.types import Message
from utilis.utilis import FormatedText
from db import Database


dataBase = Database("DB.db")
router = Router()

@router.message(Command('start'))
async def send_welcome(message : Message):
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

