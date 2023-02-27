import sqlite3 as sql
import os

DB_WORKER = None


class DBworker:
    def __init__(self, db_name):
        self.db_name = db_name

    def list_tables(self):
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result_list = [x[0] for x in cursor.fetchall()]
        return result_list

    def create(self, name):
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name} (
            test_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            old INTEGER DEFAULT 10
            )""")

    def delete(self):
        name = input(f"Список доступных баз {self.list_tables()}\n"
                     f"Введите имя удаляемой таблицы:\n")
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""DROP TABLE IF EXISTS {name}""")


def list_dbs():
    return [x for x in os.listdir() if x.endswith(".db")]


def get_db_name():
    print(f"Список доступных баз {list_dbs()}\n"
          f"Введите имя существующей либо новой базы:")
    while True:
        db_name = str(input()).strip()
        if db_name == "":
            print("Строка не должна быть пустой")
            continue
        break
    if not db_name.endswith(".db"):
        db_name += ".db"
    return db_name


def get_user_choice(worker):
    text = "Для получения списка таблиц введите : 1\n" \
           "Для добавления таблицы введите      : 2\n" \
           "Для удаления таблицы введите        : 3\n" \
           "Для редактирования таблицы введите  : 4\n" \
           "Для выхода из программы введите     : 0\n"
    print(text)
    choice = num_input_check(5)
    if choice == 1:
        print(worker.list_tables())
    if choice == 2:
        return worker.create()
    if choice == 3:
        return worker.delete()
    if choice == 4:
        pass
    if choice == 0:
        print("Выход.")
        return exit(0)


def num_input_check(end_range_num, start_range_num=0):
    while True:
        choice = input()
        if choice.strip().isdigit() and int(choice.strip()) \
                in range(start_range_num, end_range_num):
            return int(choice.strip())
        print("Неверный ввод.")
        continue


def check_name_table():
    while True:
        name = str(input("Введите имя новой таблицы:\n")).strip()
        if name[0].isdigit():
            print("Имя не может начинаться с цифры.")
            continue
        if name == "":
            print("Строка не должна быть пустой")
        if name in DB_WORKER.list_tables():
            print(f"Список таблиц: {DB_WORKER.list_tables()}\n"
                  f"Таблица с таким именем уже существует.")
            continue
        break


def main():
    global DB_WORKER
    DB_WORKER = DBworker(get_db_name())
    while True:
        get_user_choice(DB_WORKER)
        print("Выполнить еще операцию?\n"
              "да: 1, нет: 2")
        continue_choice = num_input_check(3, 1)
        if continue_choice == 1:
            continue
        if continue_choice == 2:
            exit(0)


if __name__ == '__main__':
    main()
