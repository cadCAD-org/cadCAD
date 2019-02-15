# SimCad
**Warning**:
**Do not** publish this package / software to **any** software repository **except** one permitted by BlockScience.  

**Description:**

SimCAD is a differential games based simulation software package for research, validation, and Computer \
Aided Design of economic systems. An economic system is treated as a state based model and defined through a \
set of endogenous and exogenous state variables which are updated through mechanisms and environmental \
processes, respectively. Behavioral models, which may be deterministic or stochastic, provide the evolution of \
the system within the action space of the mechanisms. Mathematical formulations of these economic games \
treat agent utility as derived from state rather than direct from action, creating a rich dynamic modeling framework.

Simulations may be run with a range of initial conditions and parameters for states, behaviors, mechanisms, \
and environmental processes to understand and visualize network behavior under various conditions. Support for \
A/B testing policies, monte carlo analysis and other common numerical methods is provided.

SimCAD is written in Python 3.

**1. Install Dependencies:**
```bash
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/cadCAD-0.2-py3-none-any.whl
```

**2. Configure Simulation:**

Intructions:
`/Simulation.md`

Examples:
`/simulations/validation/*`

**3. Import SimCAD & Run Simulation:**

Examples: `/simulations/example_run.py` or `/simulations/example_run.ipynb`

`/simulations/example_run.py`:
```python
import pandas as pd
from tabulate import tabulate

# The following imports NEED to be in the exact order
from SimCAD.engine import ExecutionMode, ExecutionContext, Executor
from validation import config1, config2
from SimCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution 1")
print()
first_config = [configs[0]] # from config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run1 = Executor(exec_context=single_proc_ctx, configs=first_config)
run1_raw_result, tensor_field = run1.main()
result = pd.DataFrame(run1_raw_result)
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
```

The above can be run in Jupyter.
```bash
jupyter notebook
```
