# cadCAD
**Warning**:
**Do not** publish this package / software to **any** software repository **except** one permitted by BlockScience.  

**Description:**

cadCAD is a differential games based simulation software package for research, validation, and Computer \
Aided Design of economic systems. An economic system is treated as a state based model and defined through a \
set of endogenous and exogenous state variables which are updated through mechanisms and environmental \
processes, respectively. Behavioral models, which may be deterministic or stochastic, provide the evolution of \
the system within the action space of the mechanisms. Mathematical formulations of these economic games \
treat agent utility as derived from state rather than direct from action, creating a rich dynamic modeling framework.

Simulations may be run with a range of initial conditions and parameters for states, behaviors, mechanisms, \
and environmental processes to understand and visualize network behavior under various conditions. Support for \
A/B testing policies, monte carlo analysis and other common numerical methods is provided.


**1. Install Dependencies:**

**Option A:** Package Repository Access

***IMPORTANT NOTE:*** Tokens are issued to and meant to be used by trial users and BlockScience employees **ONLY**. Replace \<TOKEN\> with an issued token in the script below.
```bash
pip3 install pandas pathos fn tabulate
pip3 install cadCAD --extra-index-url https://<TOKEN>@repo.fury.io/blockscience/
```

**Option B:** Build From Source
```bash
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl
```

**2. Configure Simulation:**

Intructions:
`/Simulation.md`

Examples:
`/simulations/validation/*`

**3. Import cadCAD & Run Simulations:**

Examples: `/simulations/*.py` or `/simulations/*.ipynb`

Single Simulation: `/simulations/single_config_run.py`
```python
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import config1
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run1 = Executor(exec_context=single_proc_ctx, configs=first_config)
run1_raw_result, tensor_field = run1.main()
result = pd.DataFrame(run1_raw_result)
print()
print("Tensor Field: config1")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
```

Parameter Sweep Simulation (Concurrent): `/simulations/param_sweep_run.py`
```python
import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import sweep_config
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Concurrent Execution")
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run2 = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
config_names = ['sweep_config_A', 'sweep_config_B']
for raw_result, tensor_field in run2.main():
    result = pd.DataFrame(raw_result)
    print()
    print("Tensor Field: " + config_names[i])
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    i += 1
```

Multiple Simulations (Concurrent): `/simulations/multi_config run.py`
```python
import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import config1, config2
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Concurrent Execution")
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run2 = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
config_names = ['config1', 'config2']
for raw_result, tensor_field in run2.main():
    result = pd.DataFrame(raw_result)
    print()
    print("Tensor Field: " + config_names[i])
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    i =+ 1
```

The above can be run in Jupyter.
```bash
jupyter notebook
```
