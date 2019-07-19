import unittest
from pprint import pprint

import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests import external_dataset
from cadCAD import configs
from testing.generic_test import make_generic_test
from testing.utils import gen_metric_dict

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=first_config)

raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)

# print(tabulate(result, headers='keys', tablefmt='psql'))

# cols = ['run', 'substep', 'timestep', 'increment', 'external_data', 'policies']
# result = result[cols]
#
# metrics = gen_metric_dict(result, ['increment', 'external_data', 'policies'])
# #
# pprint(metrics)

def get_expected_results(run):
    return {
        (run, 0, 0): {
            'external_data': {'ds1': None, 'ds2': None, 'ds3': None},
            'increment': 0,
            'policies': {'ds1': None, 'ds2': None, 'ds3': None}
        },
        (run, 1, 1): {
            'external_data': {'ds1': 0, 'ds2': 0, 'ds3': 1},
             'increment': 1,
             'policies': {'ds1': 0, 'ds2': 0, 'ds3': 1}
        },
        (run, 1, 2): {
            'external_data': {'ds1': 1, 'ds2': 40, 'ds3': 5},
             'increment': 2,
             'policies': {'ds1': 1, 'ds2': 40, 'ds3': 5}
        },
        (run, 1, 3): {
            'external_data': {'ds1': 2, 'ds2': 40, 'ds3': 5},
             'increment': 3,
             'policies': {'ds1': 2, 'ds2': 40, 'ds3': 5}
        },
        (run, 2, 1): {
            'external_data': {'ds1': 3, 'ds2': 40, 'ds3': 5},
             'increment': 4,
             'policies': {'ds1': 3, 'ds2': 40, 'ds3': 5}
        },
        (run, 2, 2): {
            'external_data': {'ds1': 4, 'ds2': 40, 'ds3': 5},
             'increment': 5,
             'policies': {'ds1': 4, 'ds2': 40, 'ds3': 5}
        },
        (run, 2, 3): {
            'external_data': {'ds1': 5, 'ds2': 40, 'ds3': 5},
            'increment': 6,
            'policies': {'ds1': 5, 'ds2': 40, 'ds3': 5}
        },
        (run, 3, 1): {
            'external_data': {'ds1': 6, 'ds2': 40, 'ds3': 5},
            'increment': 7,
            'policies': {'ds1': 6, 'ds2': 40, 'ds3': 5}
        },
        (run, 3, 2): {
            'external_data': {'ds1': 7, 'ds2': 40, 'ds3': 5},
            'increment': 8,
            'policies': {'ds1': 7, 'ds2': 40, 'ds3': 5}
        },
        (run, 3, 3): {
            'external_data': {'ds1': 8, 'ds2': 40, 'ds3': 5},
            'increment': 9,
            'policies': {'ds1': 8, 'ds2': 40, 'ds3': 5}
        },
        (run, 4, 1): {
            'external_data': {'ds1': 9, 'ds2': 40, 'ds3': 5},
            'increment': 10,
            'policies': {'ds1': 9, 'ds2': 40, 'ds3': 5}
        },
        (run, 4, 2): {
            'external_data': {'ds1': 10, 'ds2': 40, 'ds3': 5},
            'increment': 11,
            'policies': {'ds1': 10, 'ds2': 40, 'ds3': 5}
        },
        (run, 4, 3): {
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

# print()
# print("Tensor Field: config1")
# print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
# print("Output:")
# print(tabulate(result, headers='keys', tablefmt='psql'))
# print()
