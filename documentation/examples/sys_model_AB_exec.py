import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A, sys_model_B
from cadCAD import configs

exec_mode = ExecutionMode()

# # Multiple Processes Execution using Multiple System Model Configurations:
# # sys_model_A & sys_model_B
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
sys_model_AB_simulation = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
config_names = ['sys_model_A', 'sys_model_B']
for sys_model_AB_raw_result, sys_model_AB_tensor_field in sys_model_AB_simulation.execute():
    sys_model_AB_result = pd.DataFrame(sys_model_AB_raw_result)
    print()
    print(f"Tensor Field: {config_names[i]}")
    print(tabulate(sys_model_AB_tensor_field, headers='keys', tablefmt='psql'))
    print("Result: System Events DataFrame:")
    print(tabulate(sys_model_AB_result, headers='keys', tablefmt='psql'))
    print()
    i += 1