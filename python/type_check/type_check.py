from inspect import signature
from typing import List
from unittest import TestCase

def type_check(call):
    def wapper(*args, **kwargs):
        sig = signature(call)
        for arg, param in zip(args, sig.parameters.values()):
            if not isinstance(arg, param.annotation):
                raise TypeError(
                    "Parameter '%s' type must be %s, not %s" % \
                    (param.name, param.annotation, type(arg)))
        for key, arg in kwargs.items():
            if key in sig.parameters:
                param = sig.parameters.get(key)
            else:
                continue
            if not isinstance(arg, param.annotation):
                raise TypeError(
                    "Parameter '%s' type must be %s, not %s" % \
                    (param.name, param.annotation, type(arg)))
        result = call(*args, **kwargs)
        # if not isinstance(result, sig.return_annotation):
        #     raise TypeError('Return type must be %s, not %s' % (sig.return_annotation, type(result)))
        return result
    return wapper


@type_check
def check_base_type_param(a: int, b: str, c: bool, d: float):
    return 1


class TypeCheckTest(TestCase):
    def test_base_type_param(self):
        valid_args = [1, 'a', True, 1.1]
        self.assertEqual(check_base_type_param(*valid_args), 1)
        invalid_args = valid_args.copy()
        invalid_args[0] = '1'
        self.assertRaises(TypeError, check_base_type_param, *invalid_args)
        invalid_args[1] = 1
        self.assertRaises(TypeError, check_base_type_param, *invalid_args)
        invalid_args[2] = 'a'
        self.assertRaises(TypeError, check_base_type_param, *invalid_args)
        invalid_args[3] = 1
        self.assertRaises(TypeError, check_base_type_param, *invalid_args)
