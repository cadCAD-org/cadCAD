import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A
from cadCAD import configs

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
# sys_model_A
sys_model_A = [configs[0]] # sys_model_A
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
sys_model_A_simulation = Executor(exec_context=single_proc_ctx, configs=sys_model_A)

sys_model_A_raw_result, sys_model_A_tensor_field = sys_model_A_simulation.execute()
sys_model_A_result = pd.DataFrame(sys_model_A_raw_result)
print()
print("Tensor Field: config1")
print(tabulate(sys_model_A_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame")
print(tabulate(sys_model_A_result, headers='keys', tablefmt='psql'))
print()