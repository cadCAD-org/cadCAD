import unittest
from pprint import pprint

import pandas as pd

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.models import param_sweep
from cadCAD import configs

from testing.generic_test import make_generic_test
from testing.models.param_sweep import some_function, g as sweep_params


exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=configs)

# sim, run, substep, timestep
def get_expected_results(subset, run, beta, gamma):
    return {
        (subset, run, 0, 0): {'policies': {}, 'sweeped': {}, 'alpha': 0, 'beta': 0},
        (subset, run, 1, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 1, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 1, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 2, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 2, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 2, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 3, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 3, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 3, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 4, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 4, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 4, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (subset, run, 5, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta},
        (subset, run, 5, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta},
        (subset, run, 5, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta}
    }


def generate_expected(sweep_params):
    def template(sweep_params):
        subset_count = max(len(x) for x in list(sweep_params.values()))
        expected_results, expected_results_1, expected_results_2 = {}, {}, {}
        for subset in range(subset_count):
            expected_results_1a = get_expected_results(subset, 1, 2, 3)
            expected_results_1b = get_expected_results(subset, 2, 2, 3)
            expected_results_1.update(expected_results_1a)
            expected_results_1.update(expected_results_1b)

            expected_results_2 = {}
            expected_results_2a = get_expected_results(subset, 1, some_function, 4)
            expected_results_2b = get_expected_results(subset, 2, some_function, 4)
            expected_results_2.update(expected_results_2a)
            expected_results_2.update(expected_results_2b)

            expected_results.update(expected_results_1)
            expected_results.update(expected_results_2)

            yield expected_results

    merged_expected = list(template(sweep_params))
    result = {}
    for d in merged_expected:
        result.update(d)

    return result


def row(a, b):
    return a == b


def create_test_params(feature, fields):
    raw_result, tensor_fields, sessions = run.execute()
    df = pd.DataFrame(raw_result)
    expected = generate_expected(sweep_params)
    return [[feature, df, expected, fields, [row]]]


params = list(create_test_params("param_sweep", ['alpha', 'beta', 'policies', 'sweeped']))


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
