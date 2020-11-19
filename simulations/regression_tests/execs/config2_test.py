from functools import reduce
from pprint import pprint
import pandas as pd
from tabulate import tabulate

from cadCAD.configuration.utils import configs_as_dicts, configs_as_objs
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import config2
from cadCAD import configs

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
pprint(sessions)
print(tabulate(result, headers='keys', tablefmt='psql'))

print()
# print(len(configs_as_dicts(configs)))
# print(len(configs_as_dicts(configs)))

# ds = configs_as_dicts(configs)
ds = configs_as_objs(configs)
pprint(len(ds))
# new_d = dict([reduce(lambda x, y: [x, y], ds)])
# pprint(new_d)
print()
