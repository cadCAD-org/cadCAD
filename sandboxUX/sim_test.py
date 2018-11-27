import pandas as pd
from tabulate import tabulate

from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
from sandboxUX import config1, config2
# from sandboxUX import config4
from SimCAD import configs

# ToDo: pass ExecutionContext with execution method as ExecutionContext input

exec_mode = ExecutionMode()


print("Simulation Run 1")
print()
single_config = [configs[0]]
single_proc_ctx = ExecutionContext(exec_mode.single_proc)
run1 = Executor(single_proc_ctx, single_config)
run1_raw_result = run1.main()
result = pd.DataFrame(run1_raw_result)
# result.to_csv('~/Projects/DiffyQ-SimCAD/results/config4.csv', sep=',')
print(tabulate(result, headers='keys', tablefmt='psql'))
print()

print("Simulation Run 2: Pairwise Execution")
print()
multi_proc_ctx = ExecutionContext(exec_mode.multi_proc)
run2 = Executor(multi_proc_ctx, configs)
run2_raw_results = run2.main()
for raw_result in run2_raw_results:
    result = pd.DataFrame(raw_result)
    print(tabulate(result, headers='keys', tablefmt='psql'))
print()