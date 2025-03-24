from aiogram.types import Message
from db import Database
from datetime import datetime

dataBase = Database("DB.db")


class Basic:
    @staticmethod
    def swipeInt(delta):
        return 0 if delta == 1 else 1
    
    @staticmethod
    def boolToStr(word):
        return 'да' if bool(word) else 'нет'
    
class Order:
    @staticmethod
    async def format_url(message: Message) -> str:
        return f'https://t.me/{message.chat.username}' if message.chat.username != None and  message.chat.username  != '' else message.chat.url
    
    @staticmethod
    async def add_object(data, photos_str, message: Message) -> int: 
        url = await Order.format_url(message)
        ids = await dataBase.add_order(
            userid = message.chat.id,
            url =  url,
            number = data['number'],
            comment = data['coment'],
            price = data['price'],
            firstname = message.chat.first_name,
            photo = photos_str
        )
        return ids
    
    @staticmethod
    async def update_actual_time(message: Message) -> None:
        auto_allowed = await dataBase.get_settings('auto_allowed')
        if bool(auto_allowed):
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await dataBase.set_user_data(
                    userid =  message.chat.id,
                    key = "actual_time",
                    value = current_time
            )
    
    @staticmethod
    async def admin_text_add(order, message: Message) -> str:
        return f"Новая заявка:\n\nАйди = {order[0]}\nИмя = {message.chat.first_name}\nUserid = {order[1]}\nНомер = {order[2]}\nКоменнтарий = {order[3]}\nЦена = {order[4]}\nСтатус = {order[6]}"    

    @staticmethod
    async def format_photos_str(photos: list) -> str:
        return ",".join(photos)  if photos is not None else None
    
    @staticmethod
    async def get_all_orders():
        orders = await dataBase.get_all_orders_active()
        relevance_allowed = await dataBase.get_settings('relevance_allowed')
        actual_time = await dataBase.get_settings('actual_time')
        price = await dataBase.get_settings('price')
        
        orders_list = []
        
        for order in orders:
            userData = await dataBase.get_user_userid(order[1])
            if bool(relevance_allowed):
                if userData[8]:
                    stored_time = datetime.strptime(userData[8], "%Y-%m-%d %H:%M:%S")
                    now = datetime.now()
                    difference = (now - stored_time).days
                    if difference <= actual_time -1:
                        if price != None and price !=0:
                            if userData[5]:
                                stored_time = datetime.strptime(userData[5], "%Y-%m-%d %H:%M:%S")
                                now = datetime.now()
                                difference = (now - stored_time).days
                                if difference < 30:
                                    orders_list.append(order)
                        else:
                            orders_list.append(order)
            else:
                orders_list.append(order)
        return orders_list