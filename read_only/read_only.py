"""read only atrribute"""

def new_attr_setter_except(__class__, read_only_attrs=None):
    if read_only_attrs:
        read_only_attrs = frozenset(read_only_attrs)
    else:
        read_only_attrs = frozenset()

    def setter(self, name, value):
        try:
            getattr(self, name)
        except AttributeError:
            return super().__setattr__(name, value)

        if name not in read_only_attrs:
            raise AttributeError("Attribute '%s' is Read Only" % name)
        return super().__setattr__(name, value)

    return setter


def new_attr_setter_all(__class__, read_only_attrs=None):
    def setter(self, name, value):
        try:
            getattr(self, name)
        except AttributeError:
            return super().__setattr__(name, value)

        raise AttributeError("Attribute '%s' is Read Only" % name)

    return setter


def new_attr_setter_include(__class__, read_only_attrs=None):
    '返回一个setter函数，该方法即只读类的__setattr__方法，用于控制'
    if read_only_attrs:
        read_only_attrs = frozenset(read_only_attrs)
    else:
        read_only_attrs = frozenset()

    def setter(self, name, value):
        try:
            getattr(self, name)
        except AttributeError:
            return super().__setattr__(name, value)

        if name in read_only_attrs:
            raise AttributeError("Attribute '%s' is Read Only" % name)
        return super().__setattr__(name, value)

    return setter


func_map = {
    'include': new_attr_setter_include,
    'except': new_attr_setter_except,
    'all': new_attr_setter_all,
    }

def new_attr_setter(__class__, read_only_attrs=None, mode='include'):
    return func_map[mode](__class__, read_only_attrs)


class ReadOnlyMeta(type):
    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)

        read_only_attrs = attrs.get('read_only_attrs', None)
        args = [new_cls, read_only_attrs]
        if 'read_only_mode' in attrs:
            args.append(attrs['read_only_mode'])

        new_cls.__setattr__ = new_attr_setter(*args)
        new_cls.__setattr__.__module__ = attrs.get('__module__')
        new_cls.__setattr__.__qualname__ = '__setter__'
        return new_cls


class ReadOnly(metaclass=ReadOnlyMeta):
    pass


class Constant(ReadOnly):
    read_only_mode = 'all'

# global constant
c = Constant()
