from pprint import pprint

import pandas as pd
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import policy_aggregation

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=policy_aggregation.exp.configs)

raw_result, tensor_fields, _ = run.execute()
result = pd.DataFrame(raw_result)
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
print(tabulate(result, headers='keys', tablefmt='psql'))
