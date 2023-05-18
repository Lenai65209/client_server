"""БД и подстановка значений в запрос"""

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


# --------------------------Подстановка значений в запрос------------------------- #
# Такая задача требуется очень часто. Как ее решить?

# 1. C подстановкой по порядку на места знаков вопросов:
CURSOR.execute("SELECT Name FROM Artist ORDER BY Name LIMIT ?", '2')
RESULTS = CURSOR.fetchall()
print(RESULTS)  # -> [('A Aagrh!',), ('A Aagrh!',)]

# 2. C использованием именованных замен:
CURSOR.execute("SELECT Name from Artist ORDER BY Name LIMIT :limit", {"limit": 2})
RESULTS = CURSOR.fetchall()
print(RESULTS)  # -> [('A Aagrh!',), ('A Aagrh!',)]

# 3. С использованием подстановки через %:
CURSOR.execute("SELECT Name FROM Artist ORDER BY Name LIMIT %s" % '2')
RESULTS = CURSOR.fetchall()
print(RESULTS)  # -> [('A Aagrh!',), ('A Aagrh!',)]


# Вариант 1 - параметризованный запрос защитит нас от SQL-инъекций
# лучше исп-ть его
