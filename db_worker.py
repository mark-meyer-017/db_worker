import os
import sqlite3 as sql


class DBWorker:

    def __init__(self, db_name):
        self.db_name = db_name

    def list_tables(self):
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result_list = [x[0] for x in cursor.fetchall()]
        return result_list

    def create_table(self, name, columns_data):
        with sql.connect(self.db_name) as connection:
            cursor = connection.cursor()
            cursor.execute(f"""CREATE TABLE IF NOT EXISTS {name}  (
            {columns_data[0:-1]}
            )""")

    def delete(self, name):
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


def user_choice_handler(worker: DBWorker):
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
        name = check_name_created_table(worker)
        columns_data = check_columns_data()
        worker.create_table(name, columns_data)
    if choice == 3:
        print(f"Список доступных баз {worker.list_tables()}")
        name = check_name("Введите имя удаляемой таблицы:")
        worker.delete(name)
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
        if not name:
            print("Строка не должна быть пустой")
            continue
        if name[0].isdigit():
            print("Имя не может начинаться с цифры.")
            continue
        return name


def check_create_column(column_data):
    column_types = {1: "INTEGER", 2: "TEXT"}
    column_keywords = {1: "PRIMARY KEY", 2: "NOT NULL", 3: "DEFAULT"}
    column_name = check_name("Введите имя новой колонки:")
    print(f"Выберите тип колонки.\n"
          f"INTEGER : 1\n"
          f"TEXT    : 2")
    column_type = column_types[num_input_check(3, 1)]
    keywords = set()
    default_value = ""
    while True:
        print("Выберите ключ для колонки.\n"
              "PRIMARY KEY : 1\n"
              "NOT NULL    : 2\n"
              "DEFAULT     : 3")
        column_keyword = column_keywords[num_input_check(4, 1)]
        if column_keyword == column_keywords[1] and column_keyword in \
                column_data:
            print("В таблице может быть только один основной ключ.")
            continue
        if column_keyword == column_keywords[3]:
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
        if key == column_keywords[3]:
            keys += f"{key} {default_value} "
        else:
            keys += f"{key} "
    return f"{column_name} {column_type} {keys},"


def check_name_created_table(worker):
    if not isinstance(worker, DBWorker):
        raise ValueError("Incorrect worker type.")
    while True:
        name = check_name("Введите имя новой таблицы:")
        if name in worker.list_tables():
            print(f"Список таблиц: {worker.list_tables()}\n"
                  f"Таблица с таким именем уже существует.")
            continue
        return name


def check_columns_data():
    columns_data = ""
    while True:
        columns_data += check_create_column(columns_data)
        print(f"{'=' * 21}\n"
              f"Добавить еще колонку?\n"
              f"да  : 1\n"
              f"нет : 0")
        continue_choice = num_input_check(2)
        if continue_choice == 1:
            continue
        if continue_choice == 0:
            return columns_data


def main():
    db_worker = DBWorker(get_db_name())
    while True:
        user_choice_handler(db_worker)


if __name__ == '__main__':
    main()
