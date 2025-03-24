from aiogram import types
from keyboards import fabric
from utilis.utilis import FormatedText
from aiogram.fsm.context import  FSMContext
from aiogram.enums.parse_mode import ParseMode
from db import Database

dataBase = Database("DB.db")


class UserSerializer:
    def __init__(self, message: types.Message):

        self.chat = message.chat
        self.id = self.chat.id
        self.username = self.chat.username
        self.first_name = self.chat.first_name
        self.last_name = self.chat.last_name
        self.user = None

    async def initDb(self):
        self.user = await dataBase.add_user(
            self.id,
            self.first_name,
            self.last_name
        )
        return self.user
   
    async def get_role(self):
        if self.user == None:
            await self.initDb() 
        return self.user[4]  

    async def set_role(self, role):
        await dataBase.set_user_role(
            userid = self.id,
            role = role
        )
        return True

    async def get_json(self):
        return {
            "user_id":self.id,
            "username":self.username,
            "firstName":self.first_name
        }
    
class PeganatorMessageSerializer:
    def __init__(self,call : types.CallbackQuery,state: FSMContext):
        self.call  = call
        self.user = UserSerializer(call.message)
        self.text = ""
        self.last = ''
        self.page = 0
        self.date = []
        self.id = 0
        self.state = state

    async def callEditText(self):
        self.text = FormatedText.formatMarkdownV2(text=self.text)
        message =  await self.call.message.edit_text(
            self.text,
            reply_markup=fabric.pagination(self.page,self.id,self.last,self.date),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview = True
        )
        await self.updateLastidMessage(message)
    
    async def callAnswerMessage(self):
        self.text = FormatedText.formatMarkdownV2(text=self.text)
        message =  await self.call.bot.send_message(
            text = self.text,
            chat_id = self.user.id,
            reply_markup=fabric.pagination(self.page,self.user.id,self.last,self.date),
            parse_mode=ParseMode.MARKDOWN_V2,
            disable_web_page_preview = True,
            
        )
        await self.updateLastidMessage(message)

    async def updateLastidMessage(self,message):
        await self.state.update_data(lastid = message.message_id)