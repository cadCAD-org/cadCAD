import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests import config1, config2
from cadCAD import configs
from testing.utils import gen_metric_dict

exec_mode = ExecutionMode()

print("Simulation Execution: Concurrent Execution")
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=multi_proc_ctx, configs=configs)


def get_expected_results_1(run):
    return {
        (run, 0, 0): {'s1': 0, 's2': 0.0, 's3': 5},
        (run, 1, 1): {'s1': 1, 's2': 4, 's3': 5},
        (run, 1, 2): {'s1': 2, 's2': 6, 's3': 5},
        (run, 1, 3): {'s1': 3, 's2': [30, 300], 's3': 5},
        (run, 2, 1): {'s1': 4, 's2': 4, 's3': 5},
        (run, 2, 2): {'s1': 5, 's2': 6, 's3': 5},
        (run, 2, 3): {'s1': 6, 's2': [30, 300], 's3': 5},
        (run, 3, 1): {'s1': 7, 's2': 4, 's3': 5},
        (run, 3, 2): {'s1': 8, 's2': 6, 's3': 5},
        (run, 3, 3): {'s1': 9, 's2': [30, 300], 's3': 5},
        (run, 4, 1): {'s1': 10, 's2': 4, 's3': 5},
        (run, 4, 2): {'s1': 11, 's2': 6, 's3': 5},
        (run, 4, 3): {'s1': 12, 's2': [30, 300], 's3': 5},
        (run, 5, 1): {'s1': 13, 's2': 4, 's3': 5},
        (run, 5, 2): {'s1': 14, 's2': 6, 's3': 5},
        (run, 5, 3): {'s1': 15, 's2': [30, 300], 's3': 5},
    }

expected_results_1 = {}
expected_results_A = get_expected_results_1(1)
expected_results_B = get_expected_results_1(2)
expected_results_1.update(expected_results_A)
expected_results_1.update(expected_results_B)

expected_results_2 = {}

# print(configs)
i = 0
config_names = ['config1', 'config2']
for raw_result, tensor_field in run.execute():
    result = pd.DataFrame(raw_result)
    print()
    print(f"Tensor Field: {config_names[i]}")
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    print(gen_metric_dict)
    i += 1
