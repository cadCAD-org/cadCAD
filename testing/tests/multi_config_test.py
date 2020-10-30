import unittest
import pandas as pd

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

from testing.generic_test import make_generic_test
from testing.models import config1, config2

from cadCAD import configs

def sim_0_records(s4_var):
    init_condition_1 = {
        'timestep': 0, 'substep': 0, 's1': 0.0, 's2': 0.0, 's3': 1.0, 's4': 1.0, 'timestamp': '2018-10-01 15:16:24'
    }
    return [
        init_condition_1,
        {'timestep': 1, 'substep': 1, 's1': 1.0, 's2': 4,   's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 1, 'substep': 2, 's1': 2.0, 's2': 6,   's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 1, 'substep': 3, 's1': 3.0, 's2': 30,  's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 2, 'substep': 1, 's1': 4.0, 's2': 4,   's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
        {'timestep': 2, 'substep': 2, 's1': 5.0, 's2': 6,   's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
        {'timestep': 2, 'substep': 3, 's1': 6.0, 's2': 30,  's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
    ]

def sim_next_records(s4_var):
    init_condition_2 = {
        'timestep': 0, 'substep': 0, 's1': 0, 's2': 0, 's3': 1, 's4': 1, 'timestamp': '2018-10-01 15:16:24'
    }
    return [
        init_condition_2,
        {'timestep': 1, 'substep': 1, 's1': 1,          's2': 0,    's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 1, 'substep': 2, 's1': 'a',        's2': 0,    's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 1, 'substep': 3, 's1': ['c', 'd'], 's2': 300,  's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'timestep': 2, 'substep': 1, 's1': 1,          's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
        {'timestep': 2, 'substep': 2, 's1': 'a',        's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
        {'timestep': 2, 'substep': 3, 's1': ['c', 'd'], 's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
    ]


def get_expected_results(records, simulation, subset, run, timestep=None, substep=None):
    def record(row_dict):
        row_dict['simulation'] = simulation
        row_dict['subset'] = subset
        row_dict['run'] = run
        if timestep is not None:
            row_dict['timestep'] = timestep
        if substep is not None:
            row_dict['substep'] = substep

        return (simulation, subset, run, row_dict['timestep'], row_dict['substep']), row_dict
    return dict([record(d) for d in records])


sim_0 = get_expected_results(sim_0_records(10.43650985051199), 0, 0, 1) # 10.4365
sim_1_run_1 = get_expected_results(sim_next_records(10.43650985051199), 1, 0, 1) # 10.43650985051199
sim_1_run_2 = get_expected_results(sim_next_records(8.136507296635509), 1, 0, 2)
# expected = sim_0 + sim_1_run_1 + sim_1_run_2

expected = {}
expected.update(sim_0)
expected.update(sim_1_run_1)
expected.update(sim_1_run_2)


def row(a, b):
    return a == b


exec_mode = ExecutionMode()
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)
raw_result, tensor_fields, sessions = run.execute()
results = pd.DataFrame(raw_result)
cols = results.columns.to_list()
# key_cols = ['simulation', 'subset', 'run', 'substep', 'timestep']
# val_cols = list(set(cols) - set(key_cols))


def create_test_params(feature, results, expected, fields, eval_funcs):
    return [[feature, results, expected, fields, eval_funcs]]


params = list(create_test_params("param_sweep", results, expected, cols, [row]))


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
