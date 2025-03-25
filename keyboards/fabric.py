

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from config import  start_menu, admin_menu,\
                    verif_menu, profile_menu,\
                    admin_menulist, massAddMenu




def pagination(page: int=0,id: int=1,last:str='',elem: list=None):
    
    from callbacks.peganator import Pagination
    build = InlineKeyboardBuilder()

    if page == 0:
        if elem[0] in [ "user", "moderation" ]:
            for element in start_menu:
                build.button(
                    text = element['title'],
                    callback_data=Pagination(action = element['action'], page=page, last=last, data='')
                )
        elif elem[0] == "admin":
            for element in admin_menu:
                build.button(
                    text = element['title'],
                    callback_data=Pagination(action = element['action'], page=page, last=last, data='')
                )
        elif elem[0] == "verif":
            for element in verif_menu:
                build.button(
                    text = element['title'],
                    callback_data=Pagination(action = element['action'], page=page, last=last, data='')
                )
                

        build.adjust(1,2)

    elif page == 1:
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
            
    elif page == 2:
        build.button(
            text = "Подтвердить",
            callback_data=Pagination(action = "aprovedRegister", page=page, last="accept", data=str(elem[0]))
        )
        build.button(
            text = "Отклонить",
            callback_data=Pagination(action = "aprovedRegister", page=page, last="reject", data=str(elem[0]))
        )
        build.adjust(1)
            
    elif page == 3:
        for order in elem[id * 10:(id * 10) + 10]:
            textButton =  f"{order[2]} | {order[4]} | {order[3]}"
            build.button(
                    text = textButton,
                    callback_data=Pagination(action = "openOrder", page=page, last=last, data=f'{order[0]}')
                )
        
        if id == 0:
            button_utilis_one = InlineKeyboardButton(
                text = "⬅️ Назад",
                callback_data= "menu"
            )
        else:
            button_utilis_one = InlineKeyboardButton(
                text = "⬅️",
                callback_data= "back-page"
            )


        if last == "max":
            button_utilis_three = InlineKeyboardButton(
                text = "⠀",
                callback_data = "invisible"
            )
        else:
            button_utilis_three = InlineKeyboardButton(
                text = "➡️",
                callback_data = "next-page"
            )
            
        button_utilis_four = InlineKeyboardButton(
                text = "🔍",
                callback_data = "search"
        )      
        
        build.adjust(1)
        
        build.row(
            button_utilis_one,button_utilis_four, button_utilis_three, 
        ) 
        
    elif page == 4:
        for element in profile_menu:
            build.button(
                text = element['title'],
                callback_data=Pagination(action = element['action'], page=page, last=last, data='')
            )
        if elem[0] == 1:
            build.button(
                text = "Купить подписку",
                callback_data=Pagination(action = "buySubscribe", page=page, last=last, data='')
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 5:
        for order in elem:
            build.button(
                text = f"{order[2]}",
                callback_data=Pagination(action = "deleateOrder", page=page, last=last, data=f'{order[0]}')
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 6:
        for order in elem:
            build.button(
                text = f"{order[2]}",
                callback_data=Pagination(action = "getOrder", page=page, last=last, data=f'{order[0]}')
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
        
    elif page == 7:
        build.button(
            text = "Изменить номер",
            callback_data=Pagination(action = "editOrder", page=page, last=last, data='')
        )
        build.button(
            text = "Удалить номер",
            callback_data=Pagination(action = "deleateOrder", page=page, last=last, data=f'{elem[0]}')
        )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 8:
        build.button(
            text = "Изменить номер",
            callback_data=Pagination(action = "editOrderAccept", page=page, last=last, data='number')
        )
        
        build.button(
            text = "Изменить стоимость",
            callback_data=Pagination(action = "editOrderAccept", page=page, last=last, data='price')
        )
        
        build.button(
            text = "Изменить коментарий",
            callback_data=Pagination(action = "editOrderAccept", page=page, last=last, data='comment')
        )
        
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 9:
        build.button(
            text = "Подтвердить",
            callback_data=Pagination(action = "aprovedNumber", page=page, last="accept", data=str(elem[0]))
        )
        build.button(
            text = "Отклонить",
            callback_data=Pagination(action = "aprovedNumber", page=page, last="reject", data=str(elem[0]))
        )
        build.adjust(1)
    
    elif page == 10:
        for element in admin_menulist:
            build.button(
                text = element['title'],
                callback_data=Pagination(action = element['action'], page=page, last=last, data='')
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 11:
        for user in elem:
            build.button(
                text = f"{user[2]} | {user[1]}",
                callback_data=Pagination(action = "setUserRole", page=page, last='user', data=f'{user[1]}')
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 12:
        for payment in elem:
            build.button(
                text = payment,
                callback_data=Pagination(action = "createPay", page=page, last='', data=payment)
            )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(2)
    
    elif page == 13:
        build.button(
            text = "Оплатить!",
            url = elem[0]['payment_url']
        )
        build.button(
            text = "Проверить оплату",
            callback_data=Pagination(action = "checkPay", page=page, last=last, data=str(elem[0]['payment_id']))
        )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
        
    elif page == 14:
        build.button(
            text = "Пропустить",
            callback_data=Pagination(action = "formAddNumberPhotoSkeep", page=page, last=last, data='')
        )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1)
    
    elif page == 15:
        build.button(
            text = "Связаться",
            url = elem[0]
        )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = "deleateMessage", page=page, last=last, data='')
        )
        build.adjust(1) 
    
    elif page == 16:
        build.button(
            text = "Готово",
            callback_data=Pagination(action = "formAddNumberPhotoSkeep", page=page, last=last, data='')
        )
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        build.adjust(1) 
    
    elif page == 17:
        for order in elem[id * 10:(id * 10) + 10]:
            textButton =  f"{order[2]} | {order[4]} | {order[3]}"
            build.button(
                    text = textButton,
                    callback_data=Pagination(action = "getOrder", page=page, last=last, data=f'{order[0]}')
                )
        
        if id == 0:
            button_utilis_one = InlineKeyboardButton(
                text = "⬅️ Назад",
                callback_data= "profile"
            )
        else:
            button_utilis_one = InlineKeyboardButton(
                text = "⬅️",
                callback_data= "back-page"
            )


        if last == "max":
            button_utilis_three = InlineKeyboardButton(
                text = "⠀",
                callback_data = "invisible"
            )
        else:
            button_utilis_three = InlineKeyboardButton(
                text = "➡️",
                callback_data = "next-page"
            )
        build.adjust(1)
        build.row(
            button_utilis_one, button_utilis_three
        ) 
    
    
    elif page == 18:

        for element in massAddMenu:
            build.button(
                text = element['title'],
                callback_data=Pagination(action = element['action'], page=page, last=last, data='')
            )
            
        build.button(
            text = "⬅️ Назад",
            callback_data=Pagination(action = last, page=page, last=last, data='')
        )
        
        build.adjust(1)

    return build.as_markup(resize_keyboard=True)