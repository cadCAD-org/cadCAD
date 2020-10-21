from tabulate import tabulate
from pprint import pprint
import pandas as pd
import numpy as np
# from pandas.testing import assert_series_equal
from parameterized import parameterized, parameterized_class

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.generic_test import make_generic_test
from testing.models import config1, config2

from cadCAD import configs

import unittest

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

# raw_result, tensor_fields, sessions = run.execute()
# result = pd.DataFrame(raw_result)
# print(len(result.index))
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
# print(tabulate(result, headers='keys', tablefmt='psql'))

def sim_0_records(s4_var):
    return [
        {'substep': 0, 'timestep': 0, 's1': 0.0, 's2': 0.0, 's3': 1, 's4': 1,      'timestamp': '2018-10-01 15:16:24'},
        {'substep': 1, 'timestep': 1, 's1': 1.0, 's2': 4,   's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'substep': 2, 'timestep': 1, 's1': 2.0, 's2': 6,   's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'substep': 3, 'timestep': 1, 's1': 3.0, 's2': 30,  's3': 5, 's4': 10,     'timestamp': '2018-10-01 15:16:25'},
        {'substep': 1, 'timestep': 2, 's1': 4.0, 's2': 4,   's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
        {'substep': 2, 'timestep': 2, 's1': 5.0, 's2': 6,   's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
        {'substep': 3, 'timestep': 2, 's1': 6.0, 's2': 30,  's3': 5, 's4': s4_var, 'timestamp': '2018-10-01 15:16:26'},
    ]

def sim_1_records(s4_var):
    return [
        {'substep': 0, 'timestep': 0, 's1': 0,          's2': 0,    's3': 1, 's4': 1,       'timestamp': '2018-10-01 15:16:24'},
        {'substep': 1, 'timestep': 1, 's1': 1,          's2': 0,    's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'substep': 2, 'timestep': 1, 's1': 'a',        's2': 0,    's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'substep': 3, 'timestep': 1, 's1': ['c', 'd'], 's2': 300,  's3': 5, 's4': 10,      'timestamp': '2018-10-01 15:16:25'},
        {'substep': 1, 'timestep': 2, 's1': 1,          's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
        {'substep': 2, 'timestep': 2, 's1': 'a',        's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
        {'substep': 3, 'timestep': 2, 's1': ['c', 'd'], 's2': 300,  's3': 5, 's4': s4_var,  'timestamp': '2018-10-01 15:16:26'},
    ]

def get_expected_results(records, simulation, subset, run):

    def record(row_dict):
        row_dict['simulation'] = simulation
        row_dict['subset'] = subset
        row_dict['run'] = run
        return (simulation, subset, run, row_dict['timestep'], row_dict['substep']), row_dict

    records_dict = dict([record(d) for d in records])
    # pprint(records_dict)
    # print()
    # return records
    return records_dict

sim_0 = get_expected_results(sim_0_records(10.43650985051199), 0, 0, 1) # 10.4365
sim_1_run_1 = get_expected_results(sim_1_records(10.43650985051199), 1, 0, 1) # 10.43650985051199
sim_1_run_2 = get_expected_results(sim_1_records(8.136507296635509), 1, 0, 2)
# expected = sim_0 + sim_1_run_1 + sim_1_run_2
expected = {}
expected.update(sim_0)
expected.update(sim_1_run_1)
expected.update(sim_1_run_2)

# expected_df = pd.DataFrame(expected)
# pprint(sim)
# print(tabulate(expected_df, headers='keys', tablefmt='psql'))
# assert_series_equal(result, expected_df)

# print(result.equals(expected_df))
# cols = result.columns.to_list()
# key_cols = ['simulation', 'subset', 'run', 'substep', 'timestep']
# val_cols = list(set(cols) - set(key_cols))
# params = []
# mod_results = []
# for row in expected_df.iterrows():
#     expected_record = row[1].to_dict()
#     key = { key: expected_record[key] for key in key_cols }
#     # value = { key: expected_record[key] for key in val_cols }
#
#     record_df = result.loc[(result[list(key)] == pd.Series(key)).all(axis=1)]
#     result_record = list(record_df.T.to_dict().values())[0]
#
#     params.append((result_record, expected_record))

    # result_record['row_test'] = np.all([expected_record, result_record])

    # mod_results.append(np.all([expected_record, result_record]))

# df = pd.DataFrame(mod_results)
# print(tabulate(df, headers='keys', tablefmt='psql'))

# pprint(params)

# @parameterized_class(('result', 'expected'), params)
# class TestMathClass(unittest.TestCase):
#     def test_add(self):
#         # self.assertDictEqual(self.result, self.expected)
#         self.result == self.expected
#
# if __name__ == '__main__':
#     unittest.main()


# res = [i for i in result.columns.to_list if i not in key]
# print(list(set(result.columns.to_list()) - set(key_items)))
# print()
# print(tabulate(result, headers='keys', tablefmt='psql'))
# print()
# print(tabulate(expected_df, headers='keys', tablefmt='psql'))

# def generate_assertions_df(df, expected, evaluations):
#     test_names = []
#     for eval_f in evaluations:
#         def wrapped_eval(a, b):
#             return eval_f(a, b)
#
#         test_name = f"{eval_f.__name__}_test"
#         test_names.append(test_name)
#
#         df[test_name] = df.apply(
#             lambda x: wrapped_eval(
#                 x.to_dict(),
#                 expected[(x['simulation'], x['subset'], x['run'], x['timestep'], x['substep'])]
#             ),
#             axis=1
#         )
#
#     return df, test_names


def row(a, b):
    return a == b


# res, test_names = generate_assertions_df(result, expected, [row])
# print(tabulate(res, headers='keys', tablefmt='psql'))
# pprint(test_names)
# print(tabulate(expected_df, headers='keys', tablefmt='psql'))

raw_result, tensor_fields, sessions = run.execute()
results = pd.DataFrame(raw_result)
cols = results.columns.to_list()
key_cols = ['simulation', 'subset', 'run', 'substep', 'timestep']
val_cols = list(set(cols) - set(key_cols))
def create_test_params(feature, results, expected, fields, eval_funcs):
    return [[feature, results, expected, fields, eval_funcs]]

params = list(create_test_params("param_sweep", results, expected, cols, [row]))

class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()


