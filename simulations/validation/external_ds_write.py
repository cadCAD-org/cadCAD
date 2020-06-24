import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
# from simulations.validation import config1_test_pipe
# from simulations.validation import config1
from simulations.validation import write_simulation
from cadCAD import configs

exec_mode = ExecutionMode()

first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=first_config)

raw_result, _ = run.main()
result = pd.DataFrame(raw_result)
result.to_csv('simulations/external_data/output.csv', index=False)

print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
