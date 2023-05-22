# -------------------------- Метаклассы ----------------------------

print(' ---- Шаблон Одиночка с использованием __call__ метакласса ---- ')

# Объявляем метакласс, который будет контролировать создание нового класса
class Singleton(type):

    def __init__(self, *args, **kwargs):
        print('__init__ in Metaclass. ', self, args, kwargs)
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        print('__call__ in Metaclass')
        print(' ', self, args, kwargs)
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance


class BaseA(metaclass=Singleton):
    def __init__(self):
        print('Class BaseA')


class BaseB(metaclass=Singleton):
    def __init__(self):
        print('Class BaseB')


a_1 = BaseA()
a_2 = BaseA()

b_1 = BaseB()
b_2 = BaseB()

print('a_1 is a_2 - ', a_1 is a_2)
print('b_1 is b_2 - ', b_1 is b_2)
print('a_1 is b_1 - ', a_1 is b_1)
print('a_2 is b_2 - ', a_2 is b_2)
print('a_1 is b_2 - ', a_1 is b_2)
print('a_2 is b_1 - ', a_2 is b_1)
