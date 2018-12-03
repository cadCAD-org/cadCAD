# SimCad

**Dependencies:**
```bash
pip install -r requirements.txt
```

**Project:**

Example Runs:
`/DiffyQ-SimCAD/sandboxUX/sim_test.py`

Example Configurations:
`/DiffyQ-SimCAD/sandboxUX/connfig#.py`

**User Interface: Simulation Configuration**

Configurations:
```bash
/DiffyQ-SimCAD/ui/config.py
```

**Build Tool & Package Import:**

Step 1. Build & Install Package locally: 
```bash
pip install .
pip install -e .
```
* [Package Creation Tutorial](https://python-packaging.readthedocs.io/en/latest/minimal.html)

Step 2. Import Package & Run:  
```python
import pandas as pd
from tabulate import tabulate

# The following imports NEED to be in the exact same order
from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import config1, config2
from SimCAD import configs

# ToDo: pass ExecutionContext with execution method as ExecutionContext input

exec_mode = ExecutionMode()


print("Simulation Run 1")
print()
single_config = [configs[0]]
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run1 = Executor(exec_context=single_proc_ctx, configs=single_config)
run1_raw_result = run1.main()
result = pd.DataFrame(run1_raw_result)
# result.to_csv('~/Projects/DiffyQ-SimCAD/results/config4csv', sep=',')
print(tabulate(result, headers='keys', tablefmt='psql'))
print()

print("Simulation Run 2: Pairwise Execution")
print()
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run2 = Executor(exec_context=multi_proc_ctx, configs=configs)
run2_raw_results = run2.main()
for raw_result in run2_raw_results:
    result = pd.DataFrame(raw_result)
    print(tabulate(result, headers='keys', tablefmt='psql'))
print()
```

Same can be run in Jupyter . 
```bash
jupyter notebook
```

Notebooks Directory:  
`/DiffyQ-SimCAD/notebooks/`


**Warning**:
**Do Not** publish this package / software to **Any** software repository **except** [DiffyQ-SimCAD's staging branch](https://github.com/BlockScience/DiffyQ-SimCAD/tree/staging) or its **Fork** 
