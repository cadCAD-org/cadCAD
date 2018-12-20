import unittest

# The following imports NEED to be in the exact same order
from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
import config_test_linear_exogenous_state
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
        self.assertEqual(result['exo_state'].iloc[0], 0, "Should be 0")

    def test_last_exo_state(self):
        self.assertEqual(result['exo_state'].iloc[-1], 5, "Should be 5")

if __name__ == '__main__':
    unittest.main()
