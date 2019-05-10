from math import pi

from types import MethodType, FunctionType


def cache(func):
    data = {}
    def wrapper(*args, **kwargs):
        key = f'{func.__name__}-{str(args)}-{str(kwargs)})'
        if key in data:
            result = data.get(key)
            print('cached')
        else:
            result = func(*args, **kwargs)
            data[key] = result
            print('calculated')
        return result
    return wrapper


def method(call):
    def wrapper(*args, **kwargs):
        return call(*args, **kwargs)
    return wrapper

class Cache:
    def __init__(self, func):
        self.func = func
        self.data = {}

    def __call__(self, *args, **kwargs):
        func = self.func
        data = self.data
        key = f'{func.__name__}-{str(args)}-{str(kwargs)})'
        if key in data:
            result = data.get(key)
            print('cached')
        else:
            result = func(*args, **kwargs)
            data[key] = result
            print('calculated')
        return result

@Cache
def rectangle_area(length, width):
    return length * width


@cache
def rectangle_area(length, width):
    return length * width

rectangle_area(2, 3)
rectangle_area(2, 3)



class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width
    
    @property
    @Cache
    def area(self):
        return self.length * self.width


r = Rectangle(2, 3)
r.area()

# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "<stdin>", line 14, in __call__
# TypeError: area() missing 1 required positional argument: 'self'
