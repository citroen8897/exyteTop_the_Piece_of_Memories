import telebot
from telebot import types
import user
import main
import datetime
import time
import schedule
import sqlite3

bot = main.bot


@bot.message_handler(content_types=["text"])
def auto(message):
    print('faire auto...')
    try:
        sqlite_connection = sqlite3.connect('database.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("SELECT * FROM users")
        one_result = cursor.fetchone()
        users_data_base_all = []
        while one_result is not None:
            users_data_base_all.append([one_result[0], one_result[1],
                                        one_result[2],
                                        datetime.datetime.strptime(
                                            one_result[3],
                                            '%Y-%m-%d %H:%M:%S.%f'),
                                        one_result[4], one_result[5]])
            one_result = cursor.fetchone()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

    for person in users_data_base_all:
        heures = person[4]
        minutes = person[5]
        current_heure = datetime.datetime.now().strftime("%H")
        current_minute = datetime.datetime.now().strftime("%M")
        if current_heure == heures and current_minute == minutes:
            auto_user = user.User(person[0], person[1], person[2], person[3])
            main.push_state(message, auto_user)


schedule.every(2).seconds.do(auto)
while 1:
    schedule.run_pending()
    time.sleep(1)
