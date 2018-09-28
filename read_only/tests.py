from unittest import TestCase

from .read_only import ReadOnly, c

class A(ReadOnly):
    read_only_attrs = {'x', 'z'}
    z = 3
    def __init__(self, x, y):
        self.x = x
        self.y = y

c.TEST = True
print(c.TEST, dir(c))
# c.read_only_mode = 'asd'

# c.TEST = False

# python -m unittest discover
class ReadOnlyTest(TestCase):
    def test_read_only(self):
        a1 = A(1, 2)
        self.assert_obj_of_A(a1)
        a2 = A(1, 2)
        self.assert_obj_of_A(a2)

    def assert_obj_of_A(self, obj):
        def assignment():
            obj.x = 1
        self.assertRaises(AttributeError, assignment)
        obj.y = 100
