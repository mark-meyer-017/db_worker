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

    def create(self):
        name = check_name_created_table()
        columns_data = ""
        while True:
            columns_data += check_create_column(columns_data)
            print(f"{'='*21}\n"
                  f"Добавить еще колонку?\n"
                  f"да  : 1\n"
                  f"нет : 0")
            continue_choice = num_input_check(2)
            if continue_choice == 1:
                continue
            if continue_choice == 0:
                break
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}  (
            {columns_data[0:-1]}
            )""")

    def delete(self):
        print(f"Список доступных баз {self.list_tables()}")
        name = check_name("Введите имя удаляемой таблицы:")
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
    text = f"{'='*39}\n" \
           f"Для получения списка таблиц введите : 1\n" \
           f"Для добавления таблицы введите      : 2\n" \
           f"Для удаления таблицы введите        : 3\n" \
           f"Для редактирования таблицы введите  : 4\n" \
           f"Для выхода из программы введите     : 0"
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


def num_input_check(end_range, start_range=0):
    while True:
        choice = input()
        if choice.strip().isdigit() and int(choice.strip()) \
                in range(start_range, end_range):
            return int(choice.strip())
        print("Неверный ввод.")
        continue


def check_name(text):
    while True:
        name = str(input(f"{text}\n")).strip()
        if name == "":
            print("Строка не должна быть пустой")
            continue
        if name[0].isdigit():
            print("Имя не может начинаться с цифры.")
            continue
        return name


def check_create_column(column_data):
    COLUMN_TYPES = {1: "INTEGER", 2: "TEXT"}
    COLUMN_KEYWORDS = {1: "PRIMARY KEY", 2: "NOT NULL", 3: "DEFAULT"}
    column_name = check_name("Введите имя новой колонки:")
    print(f"Выберите тип колонки.\n"
          f"INTEGER : 1\n"
          f"TEXT: 2")
    column_type = COLUMN_TYPES[num_input_check(3, 1)]
    keywords = set()
    default_value = ""
    while True:
        print("Выберите ключ для колонки.\n"
              "PRIMARY KEY : 1\n"
              "NOT NULL    : 2\n"
              "DEFAULT     : 3")
        column_keyword = COLUMN_KEYWORDS[num_input_check(4, 1)]
        if column_keyword == COLUMN_KEYWORDS[1] and column_keyword in \
                column_data:
            print("В таблице может быть только один ключ.")
            continue
        if column_keyword == COLUMN_KEYWORDS[3]:
            print("Введите значение по умолчанию.")
            default_value = f" {input()}"
        keywords.add(column_keyword)
        print(f"Добавить еще ключ?\n"
              f"да  : 1\n"
              f"нет : 0")
        continue_choice = num_input_check(2)
        if continue_choice == 1:
            continue
        if continue_choice == 0:
            break
    keys = ""
    for key in keywords:
        if key == COLUMN_KEYWORDS[3]:
            keys += f"{key} {default_value} "
        else:
            keys += f"{key} "
    return f"{column_name} {column_type} {keys},"


def check_name_created_table():
    while True:
        name = check_name("Введите имя новой таблицы:")
        if name in DB_WORKER.list_tables():
            print(f"Список таблиц: {DB_WORKER.list_tables()}\n"
                  f"Таблица с таким именем уже существует.")
            continue
        return name


def main():
    global DB_WORKER
    DB_WORKER = DBworker(get_db_name())
    while True:
        get_user_choice(DB_WORKER)


if __name__ == '__main__':
    main()
