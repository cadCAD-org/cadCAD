import unittest
import ctypes
from copy import deepcopy
from pprint import pprint

import pandas as pd
from tabulate import tabulate

from testing.generic_test import make_generic_test
from testing.system_models.udo import run
from testing.utils import generate_assertions_df, gen_metric_dict

raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)

cols = ['increment', 'state_udo', 'state_udo_perception_tracker',
        'state_udo_tracker', 'timestamp', 'udo_policies', 'udo_policy_tracker']


# print(list(result.columns)
# ctypes.cast(id(a), ctypes.py_object).value
# pprint(gen_metric_dict(result, cols))
d = gen_metric_dict(result, cols)
pprint(d)

# for k1, v1 in d:
#     print(v1)
# d_copy = deepcopy(d)
# for k, v in d_copy.items():
#     # print(d[k]['state_udo']) # =
#     print(ctypes.cast(id(v['state_udo']['mem_id']), ctypes.py_object).value)


# pprint(d_copy)

# df = generate_assertions_df(result, d, cols)
#
# print(tabulate(df, headers='keys', tablefmt='psql'))
# 