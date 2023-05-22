# -------------------------- Метаклассы -------------------------------------

print(' ----- Демонстрация работы с методом __init__ метакласса -----')

class DocMeta(type):
    ''' Метакласс, проверяющий наличие строк документации в подконтрольном классе
    '''
    def __init__(self, clsname, bases, clsdict):
        # К моменту начала работы метода __init__ метакласса 
        # словарь атрибутов контролируемого класса уже сформирован.
        for key, value in clsdict.items():
            # Пропустить специальные и частные методы
            if key.startswith("__"): continue

            # Пропустить любые невызываемые объекты
            if not hasattr(value, "__call__"): continue

            # Проверить наличие строки документирования
            if not getattr(value, "__doc__"):
                raise TypeError("Метод %s должен иметь строку документации" % key)

        type.__init__(self, clsname, bases, clsdict)


class Documented(metaclass=DocMeta):
    ''' Базовый класс для документированных классов. Можно оставить пустым.
    '''
    pass


# Дочерний класс получает метакласс "в нагрузку" от родительского класса
class Foo(Documented):
    ''' Прикладной пользовательский класс. 
    '''
    def spam(self, a, b):
        ''' Метод spam делает кое-что '''
        pass

    def boo(self):
        print('A little problem')
