"""БД и обработка ошибок"""

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

# -----------------------------Обработка ошибок---------------------------- #

try:
    sql_statement = "INSERT INTO Artist VALUES (1, 'A Aagrh!')"
    CURSOR.execute(sql_statement)
    result = CURSOR.fetchall()
except sqlite3.DatabaseError as err:
    print("Error: ", err)  # -> Error:  UNIQUE constraint failed: Artist.ArtistId
else:
    CONN.commit()
