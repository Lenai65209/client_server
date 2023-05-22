# -------------------------- Метаклассы ----------------------------

from descriptor import TypedProperty_v2

print(' ------- Демонстрация работы с методом __new__ метакласса ----------')

class TypedMeta(type):
    ''' Метакласс, создающий список __slots__,
        который будет содержать только атрибуты типа TypedProperty
    '''
    def __new__(cls, clsname, bases, clsdict):
        slots = [ ]
        for key, value in clsdict.items():
            if isinstance(value, TypedProperty_v1):
                value.name = "_" + key
                slots.append(value.name)
        clsdict['__slots__'] = slots
        return type.__new__(cls, clsname, bases, clsdict)


class Typed(metaclass=TypedMeta):
    ''' Базовый класс для объектов, определяемых пользователем.
        Можно просто оставить пустым. Вся "магия" делается метаклассом.
    '''
    pass


# Дочерний класс получает в "наследство" также и метакласс
class Foo(Typed):
    ''' Пользовательский класс с контролируемыми атрибутами
    '''
    name = TypedProperty_v1('name', str)
    num = TypedProperty_v1('num', int, 42)
    zzz = 15


foo = Foo()

# Попытка добавить новый атрибут объекту приведёт к исключению:
# foo.xxx = 13          # <- раскомментируйте строку, чтобы увидеть исключение
# print(foo.xxx)

# Атрибут, который отсутствует в __slots__ становится read-only атрибутом
print(foo.zzz)
# foo.zzz = 77          # <- раскомментируйте строку, чтобы увидеть исключение

# При этом "легитимные" атрибуты типа TypedProperty_v1
# ведут себя обычным для атрибутов образом...
foo.num = 99
foo.name = 'Bigno!'
print(foo.num, foo.name)

# ... А также имеют дополнительные преимущества:
foo.num = 'str'
foo.name = 17
