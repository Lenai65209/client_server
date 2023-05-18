"""ORM с помощью Алхимии. Традиционный стиль"""

from sqlalchemy import __version__, create_engine, Table, Column, \
    Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

print("Версия SQLAlchemy:", __version__)  # -> Версия SQLAlchemy: 1.3.6

# -----------------------Cоздание подключений к БД-------------------------------- #
# ENGINE = create_engine('sqlite:///:memory:', echo=True)
ENGINE = create_engine('sqlite:///traditional_style_base.db3', echo=False)

# Создание подключения к локальной базе данных PostgreSQL
# ENGINE_1 = create_engine('postgresql+psycopg2://username:password@localhost:5432/mydb')

# Создание подключения к удаленной базе данных MySQL
# ENGINE_2 = create_engine('mysql+pymysql://cookiemonster:chocolatechip@mysql01.monster.internal/cookies',
# pool_recycle=3600)

print(ENGINE)  # -> Engine(sqlite:///traditional_style_base.db3)

# -----------------------------Создание таблиц------------------------------------ #
METADATA = MetaData()
users_table = Table('users', METADATA,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
    Column('password', String)
)

METADATA.create_all(ENGINE)

# ----------------------Определение класса Python для отображения в таблицу--------------------- #
# т.е. создаем шаблон записи таблицы БД

class User:
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f'<User({self.name}, {self.fullname}, {self.password})>'

# ---------------------------------Настройка отображения----------------------------------------- #
# Создание отображения
mapper(User, users_table)
USER = User("Вася", "Василий", "qweasdzxc")
# <User('Вася', 'Василий', 'qweasdzxc'>
print(USER)  # -> <User(Вася, Василий, qweasdzxc)>
# None. Как так? мы же создали объект записи и передали значения???
print(USER.id)  # -> None

# Оказывается мы еще ничего не сохранили. это нужно делать через сессии

# ------------------------------------Cоздание сессии-------------------------------------------- #
# С помощью конструктора sessionmaker создаем класс-сессия
SESSION = sessionmaker(bind=ENGINE)

# создаем объект сессии
SESS_OBJ = SESSION()

# вот теперь все хорошо
SESS_OBJ.add(USER)
SESS_OBJ.commit()
print(USER.id)  # -> 2
