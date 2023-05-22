"""Пример метакласса, переопределяющего поведение методов __new__ и __init__ своих классов"""

class MyMetaClass(type):
    # Вызывается для создания экземпляра класса, перед вызовом __init__
    def __new__(cls, name, bases, dct):
        print(f'Выделение памяти для класса {name}, '
              f'имеющего кортеж базовых классов {bases}, '
              f'и словарь атрибутов {dct}')
        return type.__new__(cls, name, bases, dct)
    def __init__(cls, name, bases, dct):
        print(f'Инициализация класса {name}')
        super(MyMetaClass, cls).__init__(name, bases, dct)


# родитель 1
class Parent_1():
    pass

# родитель 2
class Parent_2():
    pass

# пользовательский класс
class MyClass(Parent_1, Parent_2, metaclass=MyMetaClass):
    my_attr = 10

MC = MyClass()

"""
Результат:

Выделение памяти для класса MyClass, 
имеющего кортеж базовых классов (<class '__main__.Parent_1'>, <class '__main__.Parent_2'>), 
и словарь атрибутов {'__module__': '__main__', '__qualname__': 'MyClass', 'my_attr': 10}

Инициализация класса MyClass
"""