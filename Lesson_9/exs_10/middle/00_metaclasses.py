# -------------------------- Метаклассы ----------------------------

# Классы в Python - это тоже объекты. Созданием классов заведуют метаклассы.
# В обычном случае созданием классов занимается функция type

print(' ------- Создание класса функцией type ----------')

# Используя функцию type можно вот так создать новый класс:
Spam = type("Spam", (object,), {"name":'Python', "age":25})
print('Новый класс, созданный функцией type:', Spam)
print('Содержимое класса:', dir(Spam))
print('Атрибуты класса:', Spam.__dict__)
print()

# -----------------------------------------------------------------------------

print(' ------- Демонстрация очерёдности вызова методов метакласса ----------')

class Meta(type):
    @classmethod
    def __prepare__(cls, clsname, bases):
        print('>> Meta. __prepare__', cls, clsname, bases)
        return dict()

    def __new__(cls, clsname, bases, clsdict):
        print('>> Meta.__new__', cls, clsname, bases, clsdict)
        return type.__new__(cls, clsname, bases, clsdict)

    def __init__(self, *args, **kwargs):
        print('>> Meta.__init__', args, kwargs)
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('>> Meta.__call__', args, kwargs)
        return super().__call__(*args, **kwargs)

print('Перед созданием пользовательского класса Z')

class Z(metaclass=Meta):
    print('> Class Z. Начало тела класса')

    def __init__(self, x):
        print('> Z.__init__', x)
        self.x = x

    print('> Class Z. Конец тела класса')


print('\nПеред созданием экземпляра класса Z')

zorro = Z(13)
print(zorro)
