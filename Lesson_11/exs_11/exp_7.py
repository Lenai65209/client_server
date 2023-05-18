"""ORM с помощью Алхимии. Декларативный стиль"""
# Для кого-то более понятный и лаконичный

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine('sqlite:///declarative_style_base.db3', echo=False)

# Функция declarative_base(), что определяет новый класс,
# который мы назвали Base, от которого будет унаследованы все наши ORM-классы.
BASE = declarative_base()


class User(BASE):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f'<User({self.name}, {self.fullname}, {self.password})>'


USER = User("Вася", "Василий", "qweasdzxc")

BASE.metadata.create_all(ENGINE)
SESSION = sessionmaker(bind=ENGINE)
SESS_OBJ = SESSION()

SESS_OBJ.add(USER)
SESS_OBJ.commit()
print(USER.id)  # -> 2
