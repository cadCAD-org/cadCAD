import unittest
import pandas as pd

from cadCAD import configs
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.generic_test import make_generic_test

exec_mode = ExecutionMode()

first_config = configs
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=first_config)

raw_result, tensor_field, sessions = run.execute()
result = pd.DataFrame(raw_result)


def get_expected_results(run):
    return {
        (0, run, 0, 0): {
            'external_data': {'ds1': None, 'ds2': None, 'ds3': None},
            'increment': 0,
            'policies': {'ds1': None, 'ds2': None, 'ds3': None}
        },
        (0, run, 1, 1): {
            'external_data': {'ds1': 0, 'ds2': 0, 'ds3': 1},
             'increment': 1,
             'policies': {'ds1': 0, 'ds2': 0, 'ds3': 1}
        },
        (0, run, 1, 2): {
            'external_data': {'ds1': 1, 'ds2': 40, 'ds3': 5},
             'increment': 2,
             'policies': {'ds1': 1, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 1, 3): {
            'external_data': {'ds1': 2, 'ds2': 40, 'ds3': 5},
             'increment': 3,
             'policies': {'ds1': 2, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 2, 1): {
            'external_data': {'ds1': 3, 'ds2': 40, 'ds3': 5},
             'increment': 4,
             'policies': {'ds1': 3, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 2, 2): {
            'external_data': {'ds1': 4, 'ds2': 40, 'ds3': 5},
             'increment': 5,
             'policies': {'ds1': 4, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 2, 3): {
            'external_data': {'ds1': 5, 'ds2': 40, 'ds3': 5},
            'increment': 6,
            'policies': {'ds1': 5, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 3, 1): {
            'external_data': {'ds1': 6, 'ds2': 40, 'ds3': 5},
            'increment': 7,
            'policies': {'ds1': 6, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 3, 2): {
            'external_data': {'ds1': 7, 'ds2': 40, 'ds3': 5},
            'increment': 8,
            'policies': {'ds1': 7, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 3, 3): {
            'external_data': {'ds1': 8, 'ds2': 40, 'ds3': 5},
            'increment': 9,
            'policies': {'ds1': 8, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 4, 1): {
            'external_data': {'ds1': 9, 'ds2': 40, 'ds3': 5},
            'increment': 10,
            'policies': {'ds1': 9, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 4, 2): {
            'external_data': {'ds1': 10, 'ds2': 40, 'ds3': 5},
            'increment': 11,
            'policies': {'ds1': 10, 'ds2': 40, 'ds3': 5}
        },
        (0, run, 4, 3): {
            'external_data': {'ds1': 11, 'ds2': 40, 'ds3': 5},
            'increment': 12,
            'policies': {'ds1': 11, 'ds2': 40, 'ds3': 5}
        }
    }


expected_results = {}
expected_results_1 = get_expected_results(1)
expected_results_2 = get_expected_results(2)
expected_results.update(expected_results_1)
expected_results.update(expected_results_2)


def row(a, b):
    return a == b


params = [["external_dataset", result, expected_results, ['increment', 'external_data', 'policies'], [row]]]


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
