import pandas as pd
from tabulate import tabulate

# The following imports NEED to be in the exact same order
from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import config_1, config_2
from SimCAD import configs

# ToDo: pass ExecutionContext with execution method as ExecutionContext input

exec_mode = ExecutionMode()


print("Simulation Execution 1")
print()
first_config = [configs[0]] # from config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run1 = Executor(exec_context=single_proc_ctx, configs=first_config)
run1_raw_result, tensor_field = run1.main()
result = pd.DataFrame(run1_raw_result)
# result.to_csv('~/Projects/DiffyQ-SimCAD/results/config4.csv', sep=',')
print()
print("Tensor Field:")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()

print("Simulation Execution 2: Pairwise Execution")
print()
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run2 = Executor(exec_context=multi_proc_ctx, configs=configs)
for raw_result, tensor_field in run2.main():
    result = pd.DataFrame(raw_result)
    print()
    print("Tensor Field:")
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()