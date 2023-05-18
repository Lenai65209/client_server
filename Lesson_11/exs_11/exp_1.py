"""БД и запросы на выборку"""

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

# ---------------------------Запрос на выборку----------------------------- #

CURSOR.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")

RESULTS = CURSOR.fetchall()  # [('A Aagrh!',), ('A Aagrh!',), ('A Aagrh!',)] - список кортежей
RESULTS_2 = CURSOR.fetchall()  # [] - пустой список, т.к. результаты запроса уже обработаны

print(RESULTS)
print(RESULTS_2)

# или вот так

# Получение результатов #
CURSOR.execute("SELECT Name FROM Artist ORDER BY Name LIMIT 3")
print(CURSOR.fetchone())  # обрабатываем результаты запроса - "вытаскиваем" по одному объекту
print(CURSOR.fetchone())
print(CURSOR.fetchone())
print(CURSOR.fetchone())

# почему такой результат ?
"""
('A Aagrh!',)
('A Aagrh!',)
('A Aagrh!',)
None
"""

# потому к последнему шагу мы извлекли все объекты и вернулся None
