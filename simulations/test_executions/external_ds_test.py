import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests import external_dataset
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=first_config)

raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)
result = pd.concat([result, result['external_data'].apply(pd.Series)], axis=1)[
    ['run', 'substep', 'timestep', 'increment', 'external_data', 'policies', 'ds1', 'ds2', 'ds3', ]
]
print()
print("Tensor Field: config1")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
