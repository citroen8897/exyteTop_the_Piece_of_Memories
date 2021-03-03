import sqlite3
import datetime


class User:
    def __init__(self, user_id, user_lang, state_numero, last_time):
        self.user_id = user_id
        self.user_lang = user_lang
        self.state_numero = state_numero
        self.last_time = last_time
        self.users_data_base = []

    def get_users_data_base(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute("SELECT * FROM users")
            one_result = cursor.fetchone()
            while one_result is not None:
                self.users_data_base.append(User(one_result[0], one_result[1],
                                            one_result[2], one_result[3],))
                one_result = cursor.fetchone()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def verify_user(self):
        self.get_users_data_base()
        if self.user_id not in [j.user_id for j in self.users_data_base]:
            return 0
        else:
            return 1

    def add_user_data_base(self):
        current_date_time = datetime.datetime.now()
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            new_user = """INSERT INTO users(id, lang, state_numero, datetime) 
            VALUES(?, ?, ?, ?);"""
            cursor.execute(new_user, (self.user_id, self.user_lang, 1,
                                      current_date_time))
            sqlite_connection.commit()
            print("Запись успешно вставлена в таблицу users",
                  cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def get_current_user(self):
        for person in self.users_data_base:
            if person.user_id == self.user_id:
                self.user_lang = person.user_lang
                self.last_time = datetime.datetime.strptime(
                    person.last_time, '%Y-%m-%d %H:%M:%S.%f')
                self.state_numero = person.state_numero

        current_date_time = datetime.datetime.now()
        if current_date_time.strftime("%d.%m.%Y") != \
                self.last_time.strftime("%d.%m.%Y"):
            self.state_numero += 1
            self.change_user_state_numero()

    def get_state(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute(f"SELECT * FROM teachings_{self.user_lang}_1 WHERE "
                           f"daynum={self.state_numero}")
            state = cursor.fetchone()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        return state

    def change_user_state_numero(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            new_date_time = datetime.datetime.now()
            sql_update_state = "Update users set state_numero=?, datetime=? " \
                               "where id = ?"
            cursor.execute(sql_update_state,
                           (self.state_numero, new_date_time, self.user_id))
            sqlite_connection.commit()
            print("Запись успешно обновлена")
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite ", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def add_state_favorites(self, state_id):
        flag = 1
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute(f"SELECT * FROM favorites WHERE user_id={self.user_id}")
            one_result = cursor.fetchone()
            temp_list_states = []
            while one_result is not None:
                temp_list_states.append([one_result[1], one_result[2]])
                one_result = cursor.fetchone()

            if [state_id, self.user_id] not in temp_list_states:
                new_piece = """INSERT INTO favorites(state_id, user_id) 
                VALUES(?, ?);"""
                cursor.execute(new_piece, (state_id, self.user_id))
                sqlite_connection.commit()
                print("Запись успешно вставлена в таблицу favorites",
                      cursor.rowcount)
                cursor.close()
            else:
                print('Цитата уже в избранном...')
                flag = 0

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        return flag

    def get_users_favorites_states(self):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute(f"SELECT * FROM favorites WHERE user_id={self.user_id}")
            one_result = cursor.fetchone()
            temp_list_states = []
            while one_result is not None:
                temp_list_states.append(one_result[1])
                one_result = cursor.fetchone()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        return temp_list_states

    def delete_state_favorites(self, state_id):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            cursor.execute(f"DELETE FROM favorites WHERE user_id={self.user_id}, state_id={state_id}")
            sqlite_connection.commit()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")

    def add_user_alert_temps(self, user_digit, type_de_alert):
        try:
            sqlite_connection = sqlite3.connect('database.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            if type_de_alert == 'HH':
                alert_time_type = """Update users set HH=? where id = ?"""
            elif type_de_alert == 'MM':
                alert_time_type = """Update users set MM=? where id = ?"""
            cursor.execute(alert_time_type, (user_digit, self.user_id))
            sqlite_connection.commit()
            print("Запись успешно вставлена в таблицу users",
                  cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
