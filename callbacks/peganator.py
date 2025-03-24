# -*- coding: utf-8 -*-
from aiogram import Router, F, types
from aiogram.utils.keyboard import CallbackData
from aiogram.fsm.context import  FSMContext
from keyboards import fabric
from aiogram.types import CallbackQuery
from Serializers.SerializersDefauls import UserSerializer,PeganatorMessageSerializer
from utilis.utilis import FormatedText
from forms.formRegisterProfile import FormRegisterProfile
from API.SenderMessage import Notifications
from API import cryptobot 

from forms.formAddNumber import FormAddNumber
from forms.FormAddAdministrator import FormAddAdministrator
from forms.FormEditNumber import FormEditNumber
from forms.FormSetPrice import FormSetPrice
from forms.FormSetActualTime import FormSetActualTime
from forms.FormFoundMyNumber import FormFoundMyNumber
from forms.FormMassAddText import FormMassAddText
from forms.FormMassAddPhoto import FormMassAddPhoto

from main import Bot
from db import Database
from utilis.BasicFunctions import Basic, Order
from datetime import datetime

router = Router()
dataBase = Database("DB.db")

 
class Pagination(CallbackData, prefix='pag'):
    action: str
    page: int
    last : str
    data : str

async def swipeMessageKeyboard(message : types.Message, state : FSMContext,
                               page : int, this_page, pageFabric: int):
    
    last = "max" if page * 10 + 10 >= len(this_page) else "min"
    
    await message.edit_reply_markup(
        reply_markup = fabric.pagination(
            page = pageFabric,
            last = last,
            id = page,
            elem = this_page
            
            ),
    )
    
    await state.update_data(
        page = page
    )
    
@router.callback_query(F.data == "next-page")
async def pagination_handler(call: CallbackQuery,state: FSMContext):
    dataState = await state.get_data()
    pageFabric = 3
    
    if dataState['type_query'] == "list":
        this_page = await Order.get_all_orders()
    
    elif dataState['type_query'] == "search":
        this_page = await dataBase.search_orders(dataState['serach'])
    
    elif dataState['type_query'] == "searchProfile":
        this_page = await dataBase.search_orders_by_user(dataState['serach'], call.message.chat.id) 
        pageFabric = 17
    
    elif dataState["type_query"] == "profile":
        this_page = await dataBase.get_all_orders_userid(call.message.chat.id)
        pageFabric = 17
    page = dataState['page'] + 1
    
    await swipeMessageKeyboard(
        message = call.message,
        state = state,
        page = page,
        this_page = this_page,
        pageFabric = pageFabric
    )

@router.callback_query(F.data == "back-page")
async def pagination_handler(call: CallbackQuery,state: FSMContext):
    dataState = await state.get_data()
    pageFabric = 3
    if dataState['type_query'] == "list":
        this_page = await Order.get_all_orders()
    
    elif dataState['type_query'] == "search":
        this_page = await dataBase.search_orders(dataState['serach'])
    
    elif dataState['type_query'] == "searchProfile":
        this_page = await dataBase.search_orders_by_user(dataState['serach'], call.message.chat.id) 
        pageFabric = 17
    
    elif dataState["type_query"] == "profile":
        this_page = await dataBase.get_all_orders_userid(call.message.chat.id)
        pageFabric = 17
    page = max(0 , dataState['page'] - 1)
    
    await swipeMessageKeyboard(
        message = call.message,
        state = state,
        page = page,
        this_page = this_page,
        pageFabric = pageFabric
    )
    
@router.callback_query(F.data == "menu")
async def pagination_handler(call: CallbackQuery,state: FSMContext,):
    peganatorMessage = PeganatorMessageSerializer(call = call,
                                                  state = state)
    user = UserSerializer(call.message)
    await state.clear()
    peganatorMessage.text = f"*Доброго дня {user.username}!\n" \
        "Выберите интересующий пункт меню.*"
    peganatorMessage.page = 0
    peganatorMessage.last = "menu"
    peganatorMessage.date = [await user.get_role()]
    await peganatorMessage.callEditText()

@router.callback_query(F.data == "profile")
async def pagination_handler(call: CallbackQuery,state: FSMContext,):
    peganatorMessage = PeganatorMessageSerializer(call = call,
                                                  state = state)
    user = UserSerializer(call.message)
    await state.clear()
    peganatorMessage.text = "*Личный кабинет\n"
    peganatorMessage.page = 4
    peganatorMessage.last = "menu"
    userData = await dataBase.get_user_userid(userid = user.id)
    price = await dataBase.get_settings('price')
    relevance_allowed = await dataBase.get_settings('relevance_allowed')
    actual_time = await dataBase.get_settings('actual_time')
    actual_time = max(1,actual_time) if actual_time else 1
    
    if price is not None and price != 0 and price != '':
        peganatorMessage.date = [1]
        if userData[5]:
            stored_time = datetime.strptime(userData[5], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            difference = (now - stored_time).days
            if difference >=30:
                peganatorMessage.text += "Купите подписку, чтобы ваши обьявления появились.\n"
            else:
                peganatorMessage.text += f"Ваша подписка доступна {30 - difference} дней\n"
        else:
            peganatorMessage.text += "Купите подписку, чтобы ваши обьявления появились.\n"
    else:
        peganatorMessage.date = [0]
    
    if bool(relevance_allowed):
        if userData[8]:
            stored_time = datetime.strptime(userData[8], "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            difference = (now - stored_time).days
            
            if difference > actual_time - 1:
                peganatorMessage.text += "Подтвердите актуальность ваших обьявлений, чтобы они появились пользователям!*"
            else:
                peganatorMessage.text += f"Ваши обьявления еще актуальны {actual_time - difference} дня.*"
        else:
            peganatorMessage.text += "Подтвердить актуальность ваших обьявлений, чтобы они появились пользователям!*"
    else:
        peganatorMessage.text += "*"
    await peganatorMessage.callEditText()



@router.callback_query(Pagination.filter())
async def pagination_handler(call: CallbackQuery, callback_data: Pagination,state: FSMContext,bot:Bot):
    action = callback_data.action
    dataState = await state.get_data()
    user = UserSerializer(call.message)
    peganatorMessage = PeganatorMessageSerializer(call = call, state = state)
    
    if action == "menu":
        await state.clear()
        peganatorMessage.text = f"*Доброго дня {user.username}!\n" \
            "Выберите интересующий пункт меню.*"
        peganatorMessage.page = 0
        peganatorMessage.last = "menu"
        peganatorMessage.date = [await user.get_role()]
       
    elif action == "registerProfile":
        role = await user.get_role()
        peganatorMessage.page = 1
        peganatorMessage.last = "menu"
        if role == "moderation":
            peganatorMessage.text = "*У вас уже есть активная заявка на регистрацию, пожалуйста дождитесь ее решения.*"
        elif role in ['verif', 'admin']:
            peganatorMessage.text = f"*Вы уже прошли регестрацию, ваша текущая роль {role}*"
        else:
            peganatorMessage.text = "*Для регистрации укажите ваш email!*"
            await state.set_state(FormRegisterProfile.email)
    
    elif action == "aprovedRegister":
        peganatorMessage.text = "*Действие выполнено!*"
        peganatorMessage.page = -1
        peganatorMessage.last = "menu"
        text_bd = f"Пользователю с userid {callback_data.data}, {'подтвердили' if callback_data.last == 'accept' else 'отклонили'} заявку"
        await dataBase.add_archive(
            text = text_bd,
            userid = user.id
        )
        if callback_data.last == "accept":
            await dataBase.set_user_data(
                userid = callback_data.data,
                key = "role",
                value = "verif"
            )
            await bot.send_message(
                chat_id = callback_data.data,
                text = "Ваша заявка на регестрацию данных, была подтверждена!\n пропишите - \start"
            )
    
    elif action == "ordersList":
        role = await user.get_role()
        available = await dataBase.get_settings('window_allowed')
        relevance_allowed = await dataBase.get_settings('relevance_allowed')
        actual_time = await dataBase.get_settings('actual_time')
        actual_time = max(1,actual_time) if actual_time else 1
        
        if role in ['user', 'moderation'] and available == 0:
            await call.answer(
                text = "Сначала зарегистрируйтесь!",
                show_alert=True
            )
            return
        
        price = await dataBase.get_settings('price')
        orders_list = await Order.get_all_orders()
                        
        if len(orders_list) == 0:
            peganatorMessage.text = "*Пока предложений нету*"
            peganatorMessage.page = 1
            peganatorMessage.last = "menu"
        
        else:
            peganatorMessage.text = "*Нажмите на интересующие вас предложение!*"
            peganatorMessage.page = 3
            peganatorMessage.last = "menu"
            peganatorMessage.id = 0
            await state.update_data(
                page = 0,
                type_query = "list"
            )
    
            if len(orders_list) < 10:
                peganatorMessage.last = "max"
                
            peganatorMessage.date = orders_list
    
    elif action == "profile":
        peganatorMessage.page = 4
        peganatorMessage.last = "menu"
        peganatorMessage.text = "*Личный кабинет\n"
        userData = await dataBase.get_user_userid(userid = user.id)
        price = await dataBase.get_settings('price')
        relevance_allowed = await dataBase.get_settings('relevance_allowed')
        actual_time = await dataBase.get_settings('actual_time')
        actual_time = max(1,actual_time) if actual_time else 1
        
        if price is not None and price != 0 and price != '':
            peganatorMessage.date = [1]
            if userData[5]:
                stored_time = datetime.strptime(userData[5], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                difference = (now - stored_time).days
                if difference >=30:
                    peganatorMessage.text += "Купите подписку, чтобы ваши обьявления появились.\n"
                else:
                    peganatorMessage.text += f"Ваша подписка доступна {30 - difference} дней\n"
            else:
                peganatorMessage.text += "Купите подписку, чтобы ваши обьявления появились.\n"
        else:
            peganatorMessage.date = [0]
      
        if bool(relevance_allowed):
            if userData[8]:
                stored_time = datetime.strptime(userData[8], "%Y-%m-%d %H:%M:%S")
                now = datetime.now()
                difference = (now - stored_time).days
                
                if difference > actual_time - 1:
                    peganatorMessage.text += "Подтвердите актуальность ваших обьявлений, чтобы они появились пользователям!*"
                else:
                    peganatorMessage.text += f"Ваши обьявления еще актуальны {actual_time - difference} дня.*"
            else:
                peganatorMessage.text += "Подтвердить актуальность ваших обьявлений, чтобы они появились пользователям!*"
        else:
            peganatorMessage.text += "*"
        
    elif action == "deleateNumber":
        peganatorMessage.text = "*Выберите номер, который хотите удалить*"
        peganatorMessage.page = 5
        peganatorMessage.last = "profile"
        peganatorMessage.date = await dataBase.get_all_orders_userid(user.id)
        
    elif action == "deleateOrder":
        peganatorMessage.text = "*Номер успешно удален!*"
        peganatorMessage.page = 1
        peganatorMessage.last = "profile"
        await dataBase.delete_order_id(callback_data.data)
        
    elif action == "addNumber":
        peganatorMessage.text = "*Введите номер формата бцццббррр / бцццббрр.*"
        peganatorMessage.page = 1
        peganatorMessage.last = "profile"
        await state.set_state(FormAddNumber.number)
    
    elif action == "listNumbers":
        await state.clear()
        last = ""
        orders_list = await dataBase.get_all_orders_userid(user.id)
        await state.update_data(
            page = 0,
            type_query = "profile",
        )
        if len(orders_list) < 10: last = "max"
        peganatorMessage.text = "*Ваши номера*"
        peganatorMessage.page = 17
        peganatorMessage.last = last
        peganatorMessage.date = orders_list
    
    elif action == "foundMyNumber":
        await state.clear()
        peganatorMessage.text = "*Введите ваш поисковой запрос*"
        peganatorMessage.page = 1
        peganatorMessage.last = "profile"
        await state.set_state(FormFoundMyNumber.query)
    
    elif action == "getOrder":
        orderId = None
        try:
            orderId = dataState['thisOrderId']
        except:
            orderId = callback_data.data
            
        order = await dataBase.get_order_id(orderId)
        await state.update_data(thisOrderId = orderId)
        peganatorMessage.page = 7
        peganatorMessage.last = "profile"
        peganatorMessage.text = f"*Информация об номере:\n\nАйди = {order[0]}\nНомер = {order[2]}\nКоменнтарий = {order[3]}\nЦена = {order[4]}\nСтатус = {order[6]}*"    
        
        peganatorMessage.date = [order[0]]
    
    elif action == "editOrder":
        peganatorMessage.page = 8
        peganatorMessage.last = "getOrder"
        peganatorMessage.text = "*Выберите, что хотите отредактировать*"
        
    elif action == "editOrderAccept":
        peganatorMessage.text = "*Укажите новое значение*"
        peganatorMessage.page = 1
        peganatorMessage.last = "editOrder"
        await state.update_data(typeEditValue = callback_data.data)
        await state.set_state(FormEditNumber.value)
    
    elif action == "aprovedNumber":
        await call.message.delete()
        orderId = int(callback_data.data)
        status = "active" if callback_data.last == "accept" else   "denied"

        await dataBase.set_order_data(
            ids = orderId,
            key = "status",
            value = status
        )
        
        order = await dataBase.get_order_id(orderId)
        
        text_bd = f"У номера {order[2]} обнови статус. Новый статус = {status}"
        await dataBase.add_archive(
            text = text_bd,
            userid = user.id
        )
        
        await bot.send_message(
                chat_id = order[1],
                text = f"У номера {order[2]} обновился статус!\nНовый статус = {status}\nНе забывайте обнавлять актуальность номеров в профиле!"
            )
        return 

    elif action == "formAddNumberPhotoSkeep":
    
        peganatorMessage.text = "*Успешно!\nВаш товар отправлен на расмотренние администратором.*"
        peganatorMessage.page = 1
        peganatorMessage.last = "profile"
        photos = dataState.get('photos', None)
        
        photos_str = await Order.format_photos_str(photos)
        ids = await Order.add_object(dataState, photos_str, call.message)
        await Order.update_actual_time(call.message)
            
        order = await dataBase.get_order_id(ids)
        admin_text = await Order.admin_text_add(order, call.message)
        
        await Notifications.send_all_admins(
            text = admin_text,
            page = 9,
            data = [ids],
            last = "menu",
            message = call.message,
            fileid = photos
        )
        
        await state.clear()
    
    elif action == "acceptActual":

        relevance_allowed = await dataBase.get_settings('relevance_allowed')
        if bool(relevance_allowed) == False:
            return call.answer(
                show_alert=True,
                text = "Потдверждать актуальность нету необходимости."
            
        )
            

        peganatorMessage.text = "*Актуальность ваших номеров подтверждина.*"
        peganatorMessage.page = 1
        peganatorMessage.last = "profile"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        await dataBase.set_user_data(
            userid = user.id,
            key = "actual_time",
            value = current_time
        )
    
    elif action == "adminPanel":
        await state.clear()
        users = await dataBase.get_users()
        price = await dataBase.get_settings('price')
        window_allowed = await dataBase.get_settings('window_allowed')
        relevance_allowed = await dataBase.get_settings('relevance_allowed')
        auto_allowed = await dataBase.get_settings('auto_allowed')
        actual_time = await dataBase.get_settings('actual_time')
        peganatorMessage.text = f"*Выберите функцию\n\nВсего пользователей = {len(users)}\nТеукущая стоимость = {price}\nДоступность витрины всем = {Basic.boolToStr(window_allowed)}\nДоступность актуальности = {Basic.boolToStr(relevance_allowed)}\nАвто актуальность, после создания обьявления = {Basic.boolToStr(auto_allowed)}\nВремя потдверждения актуальности = {actual_time}дня*"
        peganatorMessage.page = 10
        peganatorMessage.last = "menu"
    
    elif action == "set_actual_time":
        peganatorMessage.text = "*Отправьте число - количество дней, которое будет ставиться для потдверждения актуальной информации*"
        peganatorMessage.page = 1
        peganatorMessage.last = "adminPanel"
        await state.set_state(FormSetActualTime.time)
    
    elif action == "set_window_allowed":
        
        available = await dataBase.get_settings('window_allowed')
        new_available = Basic.swipeInt(available)
        await dataBase.set_settings_data("window_allowed", new_available)
        word = Basic.boolToStr(new_available)
        peganatorMessage.page = 1
        peganatorMessage.text = f"*Вы изменили доступность витрины, новое значение = {word}*"
        peganatorMessage.last = 'adminPanel'
    
    elif action == "set_actual_allowed":
        available = await dataBase.get_settings('relevance_allowed')
        new_available = Basic.swipeInt(available)
        await dataBase.set_settings_data("relevance_allowed", new_available)
        word = Basic.boolToStr(new_available)
        peganatorMessage.page = 1
        peganatorMessage.text = f"*Вы изменили доступность актуальности, новое значение = {word}*"
        peganatorMessage.last = 'adminPanel'
        
    elif action == "set_actual_auto":
        available = await dataBase.get_settings('auto_allowed')
        new_available = Basic.swipeInt(available)
        await dataBase.set_settings_data("auto_allowed", new_available)
        word = Basic.boolToStr(new_available)
        peganatorMessage.page = 1
        peganatorMessage.text = f"*Вы изменили доступность актуальности, новое значение = {word}*"
        peganatorMessage.last = 'adminPanel'
        
    elif action == "deleateAdministrator":
        peganatorMessage.text = "*Выберите пользователя, у которого хотите забрать права администратора*" 
        peganatorMessage.page = 11
        peganatorMessage.last = "adminPanel"
        peganatorMessage.date = await dataBase.get_admins()
    
    elif action == "setUserRole":
        await dataBase.set_user_data(
            userid = callback_data.data,
            key = "role",
            value = callback_data.last
        )
        peganatorMessage.text = "*Администратор успешно удален*"
        peganatorMessage.page = 1
        peganatorMessage.last = "adminPanel"
    
    elif action == "addAdministrator":
        peganatorMessage.text = "*Укажите userid telegram пользователя, которому хотите выдать права администратора*"
        peganatorMessage.last = "adminPanel"
        peganatorMessage.page = 1
        await state.set_state(FormAddAdministrator.userid)
    
    elif action == "setPrice":
        peganatorMessage.text = "*Укажите новую стоимость в долларах за месяц ( просто число )\n 0 - значит, что подписка не нужна*"
        peganatorMessage.page = 1
        peganatorMessage.last = "adminPanel"
        await state.set_state(FormSetPrice.price)
    
    elif action == "listModerations":
        peganatorMessage.page = 1
        peganatorMessage.text = "*Список заявок модераций*"
        peganatorMessage.last = "adminPanel"
        
        ordersModerations = await dataBase.get_all_orders_moderation()
        usersModerations = await dataBase.get_users_moderations()
        userData = await dataBase.get_user_userid(user.id)
        for order in ordersModerations:
            user_delta = await dataBase.get_user_userid(order[1])
            admin_text = f"Новая заявка:\n\nАйди = {order[0]}\nИмя = {user_delta[2]}\nUserid = {order[1]}\nНомер = {order[2]}\nКоменнтарий = {order[3]}\nЦена = {order[4]}\nСтатус = {order[6]}"    
            photos = order[7]
            if photos is not None:
                photos = photos.split(',')
            await Notifications.send_notifs(
                text = admin_text,
                page = 9,
                data = [order[0]],
                last = "menu",
                message = call.message,
                users = [userData],
                fileid=photos
            )
        for userDt in  usersModerations:
            admin_text = f"Заяка!\n\nПервое имя = {userDt[2]}\nВторое имя = {userDt[3]}\nuserid = {userDt[1]}\nEmail = {userDt[7]}\nНомер телефона = {userDt[6]}"
            
            await Notifications.send_notifs(
                text = admin_text,
                page = 2,
                data = [userDt[1]],
                last = "menu",
                message = call.message,
                users = [userData]
            )
    
    elif action == "buySubscribe":
        peganatorMessage.text = "*Вы покупаете подписку на месяц!\nВыбеите валюту для оплаты*"
        # peganatorMessage.date = await cryptobot.get_available_currencies()
        peganatorMessage.page = 12
        peganatorMessage.date = ['USDT', 'TRUMP', 'TON', 'SOL', 'TRX', 'BTC', 'ETH', 'DOGE', 'LTC', 'NOT']
        peganatorMessage.last = "profile"
    
    elif action == "createPay":
        price = await dataBase.get_settings('price')
        if price != 0 and price != None:
            payUrl = await cryptobot.create_payment(
                crypto = callback_data.data,
                amount_rub = price
            )
            peganatorMessage.date = [payUrl]
            peganatorMessage.page = 13
            peganatorMessage.last = "buySubscribe"
            peganatorMessage.text = "*Оплатите по кнопке ниже и нажмите кнопку - 'проверить оплату'!*"
    
    elif action == "checkPay":
        status = await cryptobot.get_payment_status(callback_data.data)
        status = status[0]
        status = "paid"
        if status == None or status == "active":
            text = "*Оплата не найдена!\nПодождите или повторите попытку*"
            text = FormatedText.formatMarkdownV2(text)
            await bot.send_message(
                chat_id = user.id,
                text = text,
                parse_mode='MarkdownV2',
            )
            return
        else:
            if status == "paid":
                peganatorMessage.text = "*Оплата прошла вам выдали подписку на месяц!*"
                peganatorMessage.page = 1
                peganatorMessage.last = "profile"
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                await dataBase.set_user_data(
                    userid = user.id,
                    key = "payData",
                    value = current_time
                )
    
    elif action == "deleateMessage":
        messagedeleate = dataState.get('deleatemessage', None)
        if messagedeleate is not None:
            
            messagedeleate = messagedeleate.split(',')
            for message in messagedeleate:
                try:
                    await bot.delete_message(
                        chat_id = user.id,
                        message_id = message
                    )
                except:
                    pass
           
                
        await call.message.delete()
        return
    
    elif action == "openOrder":
        order = await dataBase.get_order_id(callback_data.data)
        text = f"*Номер: {order[2]}\nИмя: {order[8]}\nКомментарий: {order[3]}\nЦена: {order[4]}*"
        text = FormatedText.formatMarkdownV2(text)
        photos = []
        if order[7] is not None:
            photos = order[7].split(',')
        
        if  len(photos) == 1:
            await call.message.bot.send_photo(
                chat_id = user.id,
                photo = order[7],
                caption  = text,
                reply_markup=fabric.pagination(
                    15,
                    user.id,
                    "ordersList",
                    [order[5]]
                ),
                    parse_mode='MarkdownV2'
            )
        else:
            media = []
            for index, photo in enumerate(photos):
                if index == 0:
                    media.append(types.InputMediaPhoto(media= photo))
                else:
                    media.append(types.InputMediaPhoto(media= photo))
            if len(media) > 0:
                message = await call.message.bot.send_media_group(
                    chat_id=user.id,
                    media=media,
                )
                await state.update_data(deleatemessage=", ".join(str(msg.message_id) for msg in message))
            await call.message.bot.send_message(
                    chat_id=user.id,
                    text=text,
                    reply_markup=fabric.pagination(
                        15,
                        user.id,
                        "ordersList",
                        [order[5]]
                    ),
                    parse_mode='MarkdownV2'
                )
        return
    
    elif action == "massAdd":
        peganatorMessage.page = 18
        peganatorMessage.last = "profile"
        peganatorMessage.text = "*Выберите нужный вид массового добавления номмеров*"
        await state.clear()
    
    elif action == "massAddPhoto":
        peganatorMessage.page = 1
        peganatorMessage.last = "massAdd"
        peganatorMessage.text = "*Отправьте zip архив в формате, каждый номер - папка, название папки - значение номера и его информация(), фото в папке - фото номера. пример:\n\n1CB-120-AFS | комментарий | цена\nAS0-153-ZVX | комментарий | цена\n\nМаксимум будет принято у каждого номера 6 фото*"
        await state.clear()
        await state.set_state(FormMassAddPhoto.archive)
        
        
    elif action == "massAddText":
        peganatorMessage.page = 1
        peganatorMessage.last = "massAdd"
        peganatorMessage.text = "*Отправьте список номеров в виде сообщения, где каждый номер отдельная строка и информация отделяется через |, пример:\n\n1CB-120-AFS | комментарий | цена\nAS0-153-ZVX | комментарий | цена*"
        await state.clear()
        await state.set_state(FormMassAddText.text)
        
    await peganatorMessage.callEditText()