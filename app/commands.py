import telebot
import bd

def start(bot: telebot):
    @bot.message_handler(func=lambda m: bd.check_user(m.from_user.id) == 0 and not (m.text or "").startswith("/start"))
    def gatekeeper(message):
        bot.send_message(message.chat.id, "Привет! Чтобы начать, нажми /start 🙂")


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        user = message.from_user

        name = str(user.username) if user.username is not None else ""
        
        tg_user_id = user.id 

        bd.addUserDB(name, tg_user_id)
        bot.send_message(message.chat.id, "Добро пожаловать, я бот, буду помогать вам вести TODO список 😅")




def base(bot: telebot):      
    @bot.message_handler(commands=['help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, f"""Функционал (команды):
        \t 1. Вывести список (/mytodo)
        \t 2. Добавить задачу (/addtodo)
        \t 3. Редактировать задачу (/edittodo)
        \t 4. Удалить задачу (/deletetodo)
        \t 5. Посмотреть сколько сделано заданий (/compliteStat)
        """)


    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.send_message(message.chat.id, f"Я не понимаю: {message.text}")



def myTODO(bot: telebot):
    @bot.message_handler(commands=['mytodo'])
    def showTODO(message):
        usertodo = bd.showTodoDB(message.from_user.id)
        bot.send_message(message.chat.id, f"Вот ваш список задач:\n\n{usertodo}")



def addTODO(bot: telebot):
    @bot.message_handler(commands=['addtodo'])
    def startAddTodo(message):
        ct = bd.count_tasks(message.from_user.id)
        if ct < 30:
            bot.send_message(message.chat.id, f"Какое задание надо добавить?")
            bot.register_next_step_handler(message, getTextToTODO)
        else:
            bot.send_message(message.chat.id, f"Извините, вы достигли лимита в 30 задач")

    def getTextToTODO(message):
        texttodo = message.text
        if len(texttodo) < 401:
            tg_id = message.from_user.id 
            bd.addTodoDB(texttodo, tg_id)
            bot.send_message(message.chat.id, f"Ваше задание добавлено")
        else:
            bot.send_message(message.chat.id, f"Лимит 400 символов, сократите текст")
            bot.register_next_step_handler(message, getTextToTODO)



def deleteTODO(bot: telebot):
    @bot.message_handler(commands=['deletetodo'])
    def startDeleteTodo(message):
        usertodonumber = bd.showNumberTodoDB(message.from_user.id)
        bot.send_message(message.chat.id, f"Какую задачу хотите удалить?\n{usertodonumber}Если ошиблись, то напишите '0'")
        bot.register_next_step_handler(message, getWhatDeleteTODO)

    def getWhatDeleteTODO(message):
        tg_id = message.from_user.id 
        numbertask = message.text
        if numbertask.isdigit():
            ct = bd.count_tasks(tg_id)
            numbertask = int(numbertask)
            if numbertask == 0:
                bot.send_message(message.chat.id, f"Отмена действия")
            elif numbertask > ct:
                bot.send_message(message.chat.id, f"Введите действительный номер!")
                bot.register_next_step_handler(message, getWhatDeleteTODO)
            else:
                idLastDelTask = bd.deleteTodoDB(tg_id, numbertask)
                
                keyboard = telebot.types.InlineKeyboardMarkup()
                btn = telebot.types.InlineKeyboardButton("Отменить удаление", callback_data=f"cancelLastDel:{idLastDelTask}")
                keyboard.add(btn)

                bot.send_message(message.chat.id, f"Задание под номером {numbertask} удалено", reply_markup=keyboard)

        else:
            bot.send_message(message.chat.id, f"Введите номер!!")
            bot.register_next_step_handler(message, getWhatDeleteTODO)
    

    @bot.callback_query_handler(func=lambda call: True)
    def callback_worker(call):
        action, task_id = call.data.split(":")
        task_id = int(task_id)
        if action == "cancelLastDel":
            bd.cancelDeleteTodoDB(call.from_user.id , task_id)
            newtext = f"{call.message.text}\nP.S. Задача восставновлена"
            bot.answer_callback_query(call.id, "Отменили удаление задания")
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=newtext, reply_markup=None) 
            # убираем кнопки и меняем текст



def statTODO(bot: telebot):
    @bot.message_handler(commands=['complitestat'])
    def compliteStat(message):
        ct = bd.count_tasks(message.from_user.id, True)
        bot.send_message(message.chat.id, f"Ого, вы выполнили столько заданий: {ct}!!!")



def editTODO(bot: telebot):
    @bot.message_handler(commands=['edittodo'])
    def startEditTodo(message):
        usertodonumber = bd.showNumberTodoDB(message.from_user.id)
        bot.send_message(message.chat.id, f"Какую задачу хотите редактировать?\n{usertodonumber}Если ошиблись, то напишите '0'")
        bot.register_next_step_handler(message, getWhatEditTODO)

    
    def getWhatEditTODO(message):
        tg_id = message.from_user.id 
        numbertask = message.text
        if numbertask.isdigit():
            ct = bd.count_tasks(tg_id)
            numbertask = int(numbertask)
            if numbertask == 0:
                bot.send_message(message.chat.id, f"Отмена действия")
            elif numbertask > ct:
                bot.send_message(message.chat.id, f"Введите действительный номер!")
                bot.register_next_step_handler(message, getWhatEditTODO)
            else:
                bot.send_message(message.chat.id, f"Напишите новый текст")
                bot.register_next_step_handler(message, getTextEditTODO, numbertask)
        else:
            bot.send_message(message.chat.id, f"Введите номер!!")
            bot.register_next_step_handler(message, getWhatEditTODO)


    def getTextEditTODO(message, numbertask):
        newtext = message.text
        if len(newtext) < 401:
            tg_id = message.from_user.id 
            bd.editTodoDB(tg_id, numbertask, newtext)
            bot.send_message(message.chat.id, f"Ваше задание изменено")
        else:
            bot.send_message(message.chat.id, f"Лимит 400 символов, сократите текст")
            bot.register_next_step_handler(message, getTextEditTODO, numbertask)