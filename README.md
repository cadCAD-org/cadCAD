```
                    __________   ____ 
  ________ __ _____/ ____/   |  / __ \
 / ___/ __` / __  / /   / /| | / / / /
/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ / 
\___/\__,_/\__,_/\____/_/  |_/_____/  
by BlockScience
```

**Introduction:**

***cadCAD*** is a Python library that assists in the processes of designing, testing and validating complex systems through 
simulation. At its core, cadCAD is a differential games engine that supports parameter sweeping and Monte Carlo analyses 
and can be easily integrated with other scientific computing Python modules and data science workflows.  

**Description:**

cadCAD (complex adaptive systems computer-aided design) is a python based, unified modeling framework for stochastic 
dynamical systems and differential games for research, validation, and Computer Aided Design of economic systems created 
by BlockScience. It is capable of modeling systems at all levels of abstraction from Agent Based Modeling (ABM) to 
System Dynamics (SD), and enabling smooth integration of computational social science simulations with empirical data 
science workflows.


An economic system is treated as a state-based model and defined through a set of endogenous and exogenous state 
variables which are updated through mechanisms and environmental processes, respectively. Behavioral models, which may 
be deterministic or stochastic, provide the evolution of the system within the action space of the mechanisms. 
Mathematical formulations of these economic games treat agent utility as derived from the state rather than direct from 
an action, creating a rich, dynamic modeling framework. Simulations may be run with a range of initial conditions and 
parameters for states, behaviors, mechanisms, and environmental processes to understand and visualize network behavior 
under various conditions. Support for A/B testing policies, Monte Carlo analysis, and other common numerical methods is 
provided.


For example, cadCAD tool allows us to represent a company’s or community’s current business model along with a desired 
future state and helps make informed, rigorously tested decisions on how to get from today’s stage to the future state. 
It allows us to use code to solidify our conceptualized ideas and see if the outcome meets our expectations. We can 
iteratively refine our work until we have constructed a model that closely reflects reality at the start of the model, 
and see how it evolves. We can then use these results to inform business decisions.

#### Documentation:
* ##### [Tutorials](tutorials)
* ##### [System Model Configuration](documentation/Simulation_Configuration.md)
* ##### [System Simulation Execution](documentation/Simulation_Execution.md)
* ##### [Policy Aggregation](documentation/Policy_Aggregation.md)
* ##### [System Model Parameter Sweep](documentation/System_Model_Parameter_Sweep.md)

#### 0. Installation:

**Python 3.6.5** :: Anaconda, Inc.

**Option A:** [PyPi](https://pypi.org/project/cadCAD/): pip install
```bash
pip install cadCAD
```

**Option B:** Build From Source
```bash
pip3 install -r requirements.txt
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl
```

**Option C:** Proprietary Build Access

***IMPORTANT NOTE:*** Tokens are issued to those with access to proprietary builds of cadCAD and BlockScience employees **ONLY**. 
Replace \<TOKEN\> with an issued token in the script below.
```bash
pip3 install pandas pathos fn funcy tabulate 
pip3 install cadCAD --extra-index-url https://<TOKEN>@repo.fury.io/blockscience/
```


#### 1. [Configure System Model](documentation/Simulation_Configuration.md)

#### 2. [Execute Simulations:](documentation/Simulation_Execution.md)

##### Single Process Execution:
Example System Model Configurations: 
* [System Model A](documentation/examples/sys_model_A.py): 
`/documentation/examples/sys_model_A.py`
* [System Model B](documentation/examples/sys_model_B.py): 
`/documentation/examples/sys_model_B.py`

Example Simulation Executions:
* [System Model A](documentation/examples/sys_model_A_exec.py): 
`/documentation/examples/sys_model_A_exec.py`
* [System Model B](documentation/examples/sys_model_B_exec.py): 
`/documentation/examples/sys_model_B_exec.py`

```python
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A
from cadCAD import configs

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
# sys_model_A
sys_model_A = [configs[0]] # sys_model_A
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
sys_model_A_simulation = Executor(exec_context=single_proc_ctx, configs=sys_model_A)

sys_model_A_raw_result, sys_model_A_tensor_field = sys_model_A_simulation.execute()
sys_model_A_result = pd.DataFrame(sys_model_A_raw_result)
print()
print("Tensor Field: sys_model_A")
print(tabulate(sys_model_A_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame")
print(tabulate(sys_model_A_result, headers='keys', tablefmt='psql'))
print()
```

##### Multiple Simulations (Concurrent):
###### Multiple Simulation Execution (Multi Process Execution)
System Model Configurations: 
* [System Model A](documentation/examples/sys_model_A.py): 
`/documentation/examples/sys_model_A.py`
* [System Model B](documentation/examples/sys_model_B.py): 
`/documentation/examples/sys_model_B.py`

[Example Simulation Executions:](documentation/examples/sys_model_AB_exec.py)
`/documentation/examples/sys_model_AB_exec.py`

```python
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A, sys_model_B
from cadCAD import configs

exec_mode = ExecutionMode()

# # Multiple Processes Execution using Multiple System Model Configurations:
# # sys_model_A & sys_model_B
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
sys_model_AB_simulation = Executor(exec_context=multi_proc_ctx, configs=configs)

i = 0
config_names = ['sys_model_A', 'sys_model_B']
for sys_model_AB_raw_result, sys_model_AB_tensor_field in sys_model_AB_simulation.execute():
    sys_model_AB_result = pd.DataFrame(sys_model_AB_raw_result)
    print()
    print(f"Tensor Field: {config_names[i]}")
    print(tabulate(sys_model_AB_tensor_field, headers='keys', tablefmt='psql'))
    print("Result: System Events DataFrame:")
    print(tabulate(sys_model_AB_result, headers='keys', tablefmt='psql'))
    print()
    i += 1
```

##### Parameter Sweep Simulation (Concurrent):
[Example:](documentation/examples/param_sweep.py) 
`/documentation/examples/param_sweep.py`

```python
import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import param_sweep
from cadCAD import configs

exec_mode = ExecutionMode()
multi_proc_ctx = ExecutionContext(context=exec_mode.multi_proc)
run = Executor(exec_context=multi_proc_ctx, configs=configs)

for raw_result, tensor_field in run.execute():
    result = pd.DataFrame(raw_result)
    print()
    print("Tensor Field:")
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
```
