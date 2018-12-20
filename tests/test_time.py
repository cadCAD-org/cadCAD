import unittest

# The following imports NEED to be in the exact same order
from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
import config_test_time
from SimCAD import configs
import pandas as pd

exec_mode = ExecutionMode()
config = [configs[0]]
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=config)
raw_result, tensor_field = run.main()
result = pd.DataFrame(raw_result)

class TestTime(unittest.TestCase):

    def test_initial_condition(self):
        self.assertEqual(result['timestamp'].iloc[0], '2018-01-01 00:00:00', "Should be '2018-01-01 00:00:00'")

    def test_last_timestamp(self):
        self.assertEqual(result['timestamp'].iloc[-1], '2018-01-01 00:00:05', "Should be '2018-01-01 00:00:05'")

if __name__ == '__main__':
    unittest.main()
