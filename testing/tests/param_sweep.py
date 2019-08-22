import unittest
import pandas as pd


from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.system_models import param_sweep
from cadCAD import configs

from testing.generic_test import make_generic_test
from testing.system_models.param_sweep import some_function


exec_mode = ExecutionMode()
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=multi_proc_ctx, configs=configs)


def get_expected_results(run, beta, gamma):
    return {
        (run, 0, 0): {'policies': {}, 'sweeped': {}, 'alpha': 0, 'beta': 0},
        (run, 1, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 1, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 1, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 2, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 2, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 2, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 3, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 3, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 3, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 4, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 4, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 4, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': {'beta': beta, 'gamma': gamma}, 'alpha': 1, 'beta': beta},
        (run, 5, 1): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta},
        (run, 5, 2): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta},
        (run, 5, 3): {'policies': {'gamma': gamma, 'omega': 7}, 'sweeped': beta, 'alpha': 1, 'beta': beta}
    }


expected_results_1 = {}
expected_results_1a = get_expected_results(1, 2, 3)
expected_results_1b = get_expected_results(2, 2, 3)
expected_results_1.update(expected_results_1a)
expected_results_1.update(expected_results_1b)

expected_results_2 = {}
expected_results_2a = get_expected_results(1, some_function, 4)
expected_results_2b = get_expected_results(2, some_function, 4)
expected_results_2.update(expected_results_2a)
expected_results_2.update(expected_results_2b)


i = 0
expected_results = [expected_results_1, expected_results_2]
config_names = ['sweep_config_A', 'sweep_config_B']

def row(a, b):
    return a == b
def create_test_params(feature, fields):
    i = 0
    for raw_result, _ in run.execute():
        yield [feature, pd.DataFrame(raw_result), expected_results[i], fields, [row]]
        i += 1


params = list(create_test_params("param_sweep", ['alpha', 'beta', 'policies', 'sweeped']))


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
