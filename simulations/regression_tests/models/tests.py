import unittest

import pandas as pd
# from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD import configs

exec_mode = ExecutionMode()
first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_mode)
run = Executor(exec_context=single_proc_ctx, configs=first_config)
raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)

class TestStringMethods(unittest.TestCase):
    def __init__(self, result: pd.DataFrame, tensor_field: pd.DataFrame) -> None:
        self.result = result
        self.tensor_field = tensor_field

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()