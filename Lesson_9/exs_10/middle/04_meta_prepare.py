# -------------------------- Метаклассы ----------------------------

# Пример использования метода метакласса __prepare__
# Пример актуален для Python до версии 3.6 - 
# в Python 3.6 __prepare__ по умолчанию возвращает OrderedDict

import collections
from descriptor import TypedProperty_v2

print(' ------ Демонстрация работы с методом __prepare__ метакласса --------')


class EntityMeta(type):
    """ Метакласс для прикладных классов с контролируемыми полями
    """
    # Метод __prepare__ вызывается до чтения тела пользовательского класса,
    # возвращает объект-отображение (dict-like) для хранения атрибутов класса
    @classmethod
    def __prepare__(cls, name, bases):
        # Атрибуты класса будут теперь храниться в экземпляре OrderedDict
        return collections.OrderedDict()

    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)

        # Aтрибут _fieid_names создаётся в конструируемом классе
        cls._field_names = []
        for key, attr in clsdict.items():
            if isinstance(attr, TypedProperty_v2):
                # Заполняем список только атрибутами типа TypedProperty
                type_name = type(attr).__name__
                attr.name = '_{}_{}'.format(type_name, key)
                cls._field_names.append((key, attr.name))


class Entity(metaclass=EntityMeta):
    """ Прикладной класс с контролируемыми полями
    """
    @classmethod
    def field_names(cls):
        ''' Просто возвращает поля в порядке добавления '''
        for name in cls._field_names:
            yield name


class LineItem(Entity):
    ''' Класс-пример со множеством атрибутов
    '''
    reading_short = TypedProperty_v2(int, 13)
    description_very_long = TypedProperty_v2(str, 'Simple Line')
    here_are_numerous_simple = TypedProperty_v2(int, 1)
    price_ho_ho = TypedProperty_v2(float, 19.99)
    after_the_introduction = TypedProperty_v2(int, 73)
    await_it_is_not_a_weight = TypedProperty_v2(int, 3)


print('Атрибуты пользовательского класса: ')
# Получим все имена атрибутов класса
for field in LineItem.field_names():
    print(field)
