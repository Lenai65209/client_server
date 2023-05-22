class TypedProperty_v1:
    def __init__(self, name, type_name, default=None):
        self.name = "_" + name
        self.type = type_name
        self.default = default if default else type_name()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


class Foo:
    name = TypedProperty_v1("name", str)
    num = TypedProperty_v1("num", int, 42)


if __name__ == '__main__':
    f = Foo()
    a = f.name          # Неявно вызовет Foo.name.__get__(f,Foo)
    f.name = "Гвидо"    # Вызовет Foo.name.__set__(f,”Guido”)
    del f.name          # Вызовет Foo.name.__delete__(f)


class TypedProperty_v2:
    ''' Дескриптор атрибутов, контролирующий принадлежность указанному типу
    '''
    def __init__(self, type_name, default=None):
        self.name = None
        self.type = type_name
        if default: 
            self.default = default
        else: 
            self.default = type_name()

    def __get__(self, instance, cls):
        return getattr(instance, self.name, self.default)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError("Значение должно быть типа %s" % self.type)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        raise AttributeError("Невозможно удалить атрибут")


