import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_B
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

raw_result, tensor_field, sessions = run.execute()
result = pd.DataFrame(raw_result)
print()
print("Tensor Field: sys_model_B")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
