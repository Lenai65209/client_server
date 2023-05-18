"""БД и курсор как итератор"""

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

# ---------------------------Курсор как итератор-------------------------- #
# Использование курсора как итератора
for row in CURSOR.execute('SELECT Name FROM Artist ORDER BY Name LIMIT 3'):
    print(row)

# Полученный результат:
'''
('A Aagrh!',)
('A Aagrh!',)
('A Aagrh!',)
'''
