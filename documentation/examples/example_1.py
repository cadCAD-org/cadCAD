from pprint import pprint

import pandas as pd
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A, sys_model_B, system_model_AB_exp
from documentation.examples.sys_model_A import exp

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
# sys_model_A
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_A_simulation = Executor(exec_context=local_proc_ctx, configs=exp.configs)

sys_model_A_raw_result, sys_model_A_tensor_field, sessions = sys_model_A_simulation.execute()
sys_model_A_result = pd.DataFrame(sys_model_A_raw_result)
print()
print("Tensor Field: sys_model_A")
print(tabulate(sys_model_A_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame")
print(tabulate(sys_model_A_result, headers='keys', tablefmt='psql'))
print()

# # Multiple Processes Execution using Multiple System Model Configurations:
# # sys_model_A & sys_model_B
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
sys_model_AB_simulation = Executor(exec_context=multi_proc_ctx, configs=system_model_AB_exp.configs)

sys_model_AB_raw_result, sys_model_AB_tensor_field, sessions = sys_model_AB_simulation.execute()
print()
sys_model_AB_result = pd.DataFrame(sys_model_AB_raw_result)
print()
print(f"Tensor Field:")
print(tabulate(sys_model_AB_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame:")
print(tabulate(sys_model_AB_result, headers='keys', tablefmt='psql'))
print()
