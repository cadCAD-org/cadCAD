import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.utils import arrange_cols
from simulations.regression_tests import config2
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
single_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=single_proc_ctx, configs=configs)

for raw_result, tensor_field in run.execute():
    result = arrange_cols(pd.DataFrame(raw_result), False)
    print()
    # print("Tensor Field: " + config_names[i])
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    # i += 1
