import telebot
from telebot import types
import user
import datetime

bot = telebot.TeleBot("1630145196:AAG-vbNj8WVlZY7kYC3zpuVTHEdYUq16Fzw")


@bot.message_handler(commands=["start"])
def start(message):
    current_user = user.User(message.chat.id, 'xx', 0, datetime.datetime.now())
    if current_user.verify_user() == 0:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        callback_button_1 = types.InlineKeyboardButton(
            text="English", callback_data=1)
        callback_button_2 = types.InlineKeyboardButton(
            text="Français", callback_data=2)
        callback_button_3 = types.InlineKeyboardButton(
            text="Deutsche", callback_data=3)
        callback_button_4 = types.InlineKeyboardButton(
            text="Española", callback_data=4)
        callback_button_5 = types.InlineKeyboardButton(
            text="Русский", callback_data=5)
        callback_button_6 = types.InlineKeyboardButton(
            text="हिन्दी ", callback_data=6)
        callback_button_7 = types.InlineKeyboardButton(
            text="日本語 ", callback_data=7)
        callback_button_8 = types.InlineKeyboardButton(
            text="한국어 ", callback_data=8)
        callback_button_9 = types.InlineKeyboardButton(
            text="中国人 ", callback_data=9)

        keyboard.add(callback_button_1, callback_button_2, callback_button_3,
                     callback_button_4, callback_button_5, callback_button_6,
                     callback_button_7, callback_button_8, callback_button_9)
        bot.send_message(
            message.chat.id, "Select your language:", reply_markup=keyboard)
    else:
        print('user already in DB...')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=2)
        btn1 = types.KeyboardButton("Изменить язык")
        btn2 = types.KeyboardButton("Избранное")
        btn3 = types.KeyboardButton("Уведомления")
        btn4 = types.KeyboardButton("Поделиться")
        markup.add(btn1, btn2, btn3, btn4)
        send_mess = (
            f"Привет {message.from_user.first_name} "
            f"{message.from_user.last_name}"
        )
        bot.send_message(message.chat.id, send_mess, reply_markup=markup)

        push_state(message, current_user)


@bot.message_handler(content_types=["text"])
def step_un(message):
    un_repondre = message.text
    if un_repondre == "Изменить язык":
        pass
    elif un_repondre == "Избранное":
        get_favorites(message)
    elif un_repondre == "Уведомления":
        faire_alert(message)
    elif un_repondre == "Поделиться":
        pass
    else:
        return start


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)

    if int(call.data) in range(1, 10):
        bot.edit_message_reply_markup(
            call.message.chat.id, call.message.message_id)
        bot.delete_message(call.message.chat.id, call.message.message_id)

        if call.data == "1":
            new_user = user.User(call.message.chat.id, 'en', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "2":
            new_user = user.User(call.message.chat.id, 'fr', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "3":
            new_user = user.User(call.message.chat.id, 'de', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "4":
            new_user = user.User(call.message.chat.id, 'es', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "5":
            new_user = user.User(call.message.chat.id, 'ru', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "6":
            new_user = user.User(call.message.chat.id, 'hi', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "7":
            new_user = user.User(call.message.chat.id, 'ja', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "8":
            new_user = user.User(call.message.chat.id, 'ko', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()
        elif call.data == "9":
            new_user = user.User(call.message.chat.id, 'zh', 1,
                                 datetime.datetime.now())
            new_user.add_user_data_base()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                           row_width=2)
        btn1 = types.KeyboardButton("Изменить язык")
        btn2 = types.KeyboardButton("Избранное")
        btn3 = types.KeyboardButton("Уведомления")
        btn4 = types.KeyboardButton("Поделиться")
        markup.add(btn1, btn2, btn3, btn4)
        send_mess = (
            f"Привет {call.message.from_user.first_name} "
            f"{call.message.from_user.last_name}"
        )
        bot.send_message(call.message.chat.id, send_mess, reply_markup=markup)

        push_state(call.message, new_user)

    elif call.data == '10':
        current_user = user.User(call.message.chat.id, 'xx', 0,
                                 datetime.datetime.now())
        if current_user.verify_user():
            current_user.get_current_user()
            state = current_user.get_state()
            if current_user.add_state_favorites(state[0]):
                bot.send_message(call.message.chat.id,
                                 'Цитата добавлена в избранное...')
            else:
                bot.send_message(call.message.chat.id,
                                 'Цитата уже в избранном...')


@bot.message_handler(content_types=["text"])
def push_state(message, some_user):
    some_user.get_current_user()
    state = some_user.get_state()

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button_1 = types.InlineKeyboardButton(
        text="Добавить в избранное", callback_data=10)
    callback_button_2 = types.InlineKeyboardButton(
        text="Поделиться", callback_data=11)
    keyboard.add(callback_button_1, callback_button_2)
    bot.send_message(
        message.chat.id, state[1], reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def get_favorites(message):
    current_user = user.User(message.chat.id, 'xx', 0, datetime.datetime.now())
    if current_user.verify_user():
        current_user.get_current_user()
        user_favorites = {
            current_user.user_id: current_user.get_users_favorites_states()}
        if len(user_favorites[current_user.user_id]) == 0:
            bot.send_message(message.chat.id,
                             'Вы еще не добавляли цитаты в избранное')
        else:
            bot.send_message(message.chat.id,
                             'У Вас в избранном следующие цитаты:')
            for numero in user_favorites[current_user.user_id]:
                current_user.state_numero = numero
                state = current_user.get_state()
                bot.send_message(message.chat.id, state[1])


@bot.message_handler(content_types=["text"])
def faire_alert(message):
    msg = bot.send_message(message.chat.id,
                           "Для настройки уведомлений необходимо задать "
                           "желаемое время получения уведомлений.\n\n"
                           "Для отключения уведомлений введите 666 в ответ "
                           "на оба запроса\n\n"
                           "Введите желаемый час получения уведомлений в "
                           "формате ЧЧ")
    bot.register_next_step_handler(msg, get_min)


@bot.message_handler(content_types=["text"])
def get_min(message):
    alert_heure = message.text
    if alert_heure not in [str(j) for j in range(25)] and alert_heure != '666':
        bot.send_message(message.chat.id, 'Некорректное значение!')
        faire_alert(message)
    else:
        current_user = user.User(message.chat.id, 'xx', 0,
                                 datetime.datetime.now())
        if current_user.verify_user():
            current_user.get_current_user()
            current_user.add_user_alert_temps(alert_heure, 'HH')
            msg = bot.send_message(message.chat.id,
                                   "Введите желаемую минуту получения "
                                   "уведомлений в формате ММ")
            bot.register_next_step_handler(msg, fin_de_alert)


@bot.message_handler(content_types=["text"])
def fin_de_alert(message):
    alert_min = message.text
    if alert_min not in [str(j) for j in range(60)] and alert_min != '666':
        bot.send_message(message.chat.id, 'Некорректное значение!')
        faire_alert(message)
    else:
        current_user = user.User(message.chat.id, 'xx', 0,
                                 datetime.datetime.now())
        if current_user.verify_user():
            current_user.get_current_user()
            current_user.add_user_alert_temps(alert_min, 'MM')
            bot.send_message(message.chat.id,
                             'Время уведомлений успешно сохранено!')


if __name__ == "__main__":
    bot.polling()
