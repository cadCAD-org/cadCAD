import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import sweep_config
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Concurrent Execution")
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
config_names = ['sweep_config_A', 'sweep_config_B']
for raw_result, tensor_field in run.execute():
    result = pd.DataFrame(raw_result)
    print()
    print("Tensor Field: " + config_names[i])
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    i += 1
