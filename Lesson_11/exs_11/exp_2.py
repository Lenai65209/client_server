"""БД и запросы на изменение"""

# Подключение библиотеки, соответствующей типу требуемой базы данных
import os
import sqlite3

DB_OBJ = os.path.join(os.path.dirname(__file__), "demo.sqlite")

# Создание соединения с базой данных
# В данном случае это файл базы
CONN = sqlite3.connect(DB_OBJ)
# CONN = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

# Создаем курсор — это специальный объект,
# который делает запросы и получает их результаты
CURSOR = CONN.cursor()

# ---------------------------Запрос на изменение----------------------------- #

# Выполняется INSERT-запрос к базе данных с обычным SQL-синтаксисом
CURSOR.execute("INSERT INTO Artist VALUES (Null, 'A Aagrh!') ")

# Если выполняются изменения в базе данных, необходимо сохранить транзакцию
CONN.commit()

# Проверка результатов
CURSOR.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
RESULTS = CURSOR.fetchall()
print(RESULTS)  # -> [('A Aagrh!',), ('A Cor Do Som',), ('AC/DC',)]

# А можно ли выполнить несколько запросов за раз???

'''
CURSOR.execute("""
    INSERT INTO Artist VALUES (Null, 'A Aagrh!');
    INSERT INTO Artist VALUES (Null, 'A Aagrh-2!');
""")
'''

# Будет ошибка
# sqlite3.Warning: You can only execute one statement at a time.

# Что же делать?
# Вариант есть!

'''
CURSOR.executescript("""
    INSERT INTO Artist VALUES (Null, 'A Aagrh!');
    INSERT INTO Artist VALUES (Null, 'A Aagrh-2!');
""")
'''
