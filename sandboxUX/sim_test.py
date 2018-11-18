import pandas as pd
from tabulate import tabulate

from SimCAD.engine import ExecutionContext, Executor
from sandboxUX import config1, config2

# pass ExecutionContext function instead of class

print("Simulation Run 1")
print()
single_config = [config1]
run1 = Executor(ExecutionContext, single_config)
run1_raw_result = run1.main()
result = pd.DataFrame(run1_raw_result)
print(tabulate(result, headers='keys', tablefmt='psql'))
print()

print("Simulation Run 2: Pairwise Execution")
print()
configs = [config1, config2]
run2 = Executor(ExecutionContext, configs)
run2_raw_results = run2.main()
for raw_result in run2_raw_results:
    result = pd.DataFrame(raw_result)
    print(tabulate(result, headers='keys', tablefmt='psql'))
print()