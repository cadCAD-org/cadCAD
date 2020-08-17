import unittest
import pandas as pd

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.generic_test import make_generic_test
from testing.models import policy_aggregation
from cadCAD import configs

exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=configs)

raw_result, tensor_field, _ = run.execute()
result = pd.DataFrame(raw_result)

expected_results = {
    (0, 1, 0, 0): {'policies': {}, 's1': 0},
    (0, 1, 1, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 1}, # 'policy1': 2
    (0, 1, 1, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 2},
    (0, 1, 1, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 3},
    (0, 1, 2, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 4},
    (0, 1, 2, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 5},
    (0, 1, 2, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 6},
    (0, 1, 3, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 7},
    (0, 1, 3, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 8},
    (0, 1, 3, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 9}
}


def row(a, b):
    return a == b


params = [["policy_aggregation", result, expected_results, ['policies', 's1'], [row]]]


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
