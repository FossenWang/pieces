from unittest import TestCase

from .read_only import c



class ReadOnlyTest(TestCase):
    def test_read_only(self):
        self.assertDictEqual(c.__dict__, {})

        # 首次赋值
        c.test = 'test'
        self.assertEqual(c.test, 'test')
        self.assertDictEqual(c.__dict__, {'test': 'test'})

        # 不允许再次赋值
        def func():
            c.test = 'test'
        self.assertRaises(AttributeError, func)

        # 不允许通过__dict__修改属性
        def func():
            c.__dict__['test'] = '123'
        self.assertRaises(AttributeError, func)

        # 不允许修改__dict__
        def func():
            c.__dict__ = {'test': 'zxc'}
        self.assertRaises(AttributeError, func)

        # 不允许修改__setter__
        def func():
            c.__setattr__ = None
        self.assertRaises(AttributeError, func)
