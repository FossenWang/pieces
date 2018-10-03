"""read only atrribute"""


class ReadOnlyDict(dict):
    def __setitem__(self, key, value):
        raise AttributeError("Attribute '%s' is read-only" % key)


def new_attr_setter(cls):
    def setter(self, name, value):
        if name == '__dict__':
            if isinstance(self.__dict__, ReadOnlyDict):
                raise AttributeError("Attribute '%s' is read-only" % name)
            # 不允许随意修改__dict__属性
            super(cls, self).__setattr__(name, value)
        elif name in dir(self):
            # 不允许随意修改已有的属性
            raise AttributeError("Attribute '%s' is read-only" % name)
        else:
            super(cls, self).__setattr__(name, value)
    return setter


class ReadOnlyMeta(type):
    def __new__(cls, name, bases, attrs):
        '修改类方法__setattr__, 限制修改条件'
        new_cls = type.__new__(cls, name, bases, attrs)
        new_cls.__setattr__ = new_attr_setter(new_cls)
        new_cls.__setattr__.__module__ = attrs.get('__module__')
        new_cls.__setattr__.__qualname__ = '__setter__'
        return new_cls


class ReadOnly(metaclass=ReadOnlyMeta):
    def __new__(cls, **kwargs):
        '修改实例字典__dict__, 限制修改实例字典'
        instance = super().__new__(cls, **kwargs)
        instance.__dict__ = ReadOnlyDict(instance.__dict__)
        return instance


class Constant(ReadOnly):
    pass


# global constant
c = Constant()
