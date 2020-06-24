Simulation Execution
==
System Simulations are executed with the execution engine executor (`cadCAD.engine.Executor`) given System Model 
Configurations. There are multiple simulation Execution Modes and Execution Contexts.

### Steps:
1. #### *Choose Execution Mode*:
    * ##### Simulation Execution Modes:
        `cadCAD` executes a process per System Model Configuration and a thread per System Simulation.
    ##### Class: `cadCAD.engine.ExecutionMode`
    ##### Attributes:
    * **Local Mode (Default):** Automatically selects Single Threaded or Multi-Process/Threaded Modes (Example: 
    `cadCAD.engine.ExecutionMode().local_mode`).
    * **Single Threaded Mode:** A single threaded Execution Mode for a single System Model Configuration (Example: 
    `cadCAD.engine.ExecutionMode().single_mode`).
    * **Multi-Process/Threaded Mode:** Execution Mode for System Model Simulations which executes Multiple threads within 
    multiple processes per given System Model Configuration (Example: `cadCAD.engine.ExecutionMode().multi_mode`).
2. #### *Create Execution Context using Execution Mode:*
```python
from cadCAD.engine import ExecutionMode, ExecutionContext
exec_mode = ExecutionMode()
local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
```
3. #### *Create Simulation Executor*
```python
from cadCAD.engine import Executor
from cadCAD import configs
simulation = Executor(exec_context=local_mode_ctx, configs=configs)
```
4. #### *Execute Simulation: Produce System Event Dataset*
A Simulation execution produces a System Event Dataset and the Tensor Field applied to initial states used to create it. 
```python
import pandas as pd
raw_system_events, tensor_field, sessions = simulation.execute()

# Simulation Result Types:
# raw_system_events: List[dict] 
# tensor_field: pd.DataFrame

# Result System Events DataFrame
simulation_result = pd.DataFrame(raw_system_events)
```

##### Example Tensor Field
```
+----+-----+--------------------------------+--------------------------------+
|    |   m | b1                             | s1                             |
|----+-----+--------------------------------+--------------------------------|
|  0 |   1 | <function p1m1 at 0x10c458ea0> | <function s1m1 at 0x10c464510> |
|  1 |   2 | <function p1m2 at 0x10c464048> | <function s1m2 at 0x10c464620> |
|  2 |   3 | <function p1m3 at 0x10c464400> | <function s1m3 at 0x10c464730> |
+----+-----+--------------------------------+--------------------------------+
```

##### Example Result: System Events DataFrame
```
+----+-------+------------+-----------+------+-----------+
|    |   run |   timestep |   substep |   s1 | s2        |
|----+-------+------------+-----------+------+-----------|
|  0 |     1 |          0 |         0 |    0 | 0.0       |
|  1 |     1 |          1 |         1 |    1 | 4         |
|  2 |     1 |          1 |         2 |    2 | 6         |
|  3 |     1 |          1 |         3 |    3 | [ 30 300] |
|  4 |     2 |          0 |         0 |    0 | 0.0       |
|  5 |     2 |          1 |         1 |    1 | 4         |
|  6 |     2 |          1 |         2 |    2 | 6         |
|  7 |     2 |          1 |         3 |    3 | [ 30 300] |
+----+-------+------------+-----------+------+-----------+
```

### Execution Examples:
##### Single Simulation Execution (Single Threaded Execution)
Example System Model Configurations: 
* [System Model A](examples/sys_model_A.py): `/documentation/examples/sys_model_A.py`
* [System Model B](examples/sys_model_B.py): `/documentation/examples/sys_model_B.py`
Example Simulation Executions:
* [System Model A](examples/sys_model_A_exec.py): `/documentation/examples/sys_model_A_exec.py`
* [System Model B](examples/sys_model_B_exec.py): `/documentation/examples/sys_model_B_exec.py`
```python
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A
from cadCAD import configs

exec_mode = ExecutionMode()

# Single Process Execution using a Single System Model Configuration:
# sys_model_A
local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_A_simulation = Executor(exec_context=local_mode_ctx, configs=configs)

sys_model_A_raw_result, sys_model_A_tensor_field, sessions = sys_model_A_simulation.execute()
sys_model_A_result = pd.DataFrame(sys_model_A_raw_result)
print()
print("Tensor Field: sys_model_A")
print(tabulate(sys_model_A_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame")
print(tabulate(sys_model_A_result, headers='keys', tablefmt='psql'))
print()
```

##### Multiple Simulation Execution

* ##### *Multi-Process / Threaded Execution*
Documentation: Simulation Execution 
[Example Simulation Executions::](examples/sys_model_AB_exec.py) `/documentation/examples/sys_model_AB_exec.py`
Example System Model Configurations: 
* [System Model A](examples/sys_model_A.py): `/documentation/examples/sys_model_A.py`
* [System Model B](examples/sys_model_B.py): `/documentation/examples/sys_model_B.py`
```python
import pandas as pd
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import sys_model_A, sys_model_B
from cadCAD import configs

exec_mode = ExecutionMode()

# # Multiple Processes Execution using Multiple System Model Configurations:
# # sys_model_A & sys_model_B
local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
sys_model_AB_simulation = Executor(exec_context=local_mode_ctx, configs=configs)

sys_model_AB_raw_result, sys_model_AB_tensor_field, sessions = sys_model_AB_simulation.execute()
sys_model_AB_result = pd.DataFrame(sys_model_AB_raw_result)
print()
print(f"Tensor Field:")
print(tabulate(sys_model_AB_tensor_field, headers='keys', tablefmt='psql'))
print("Result: System Events DataFrame:")
print(tabulate(sys_model_AB_result, headers='keys', tablefmt='psql'))
print()
```

* ##### [*System Model Parameter Sweep*](System_Model_Parameter_Sweep.md) 

[Example:](examples/param_sweep.py) `/documentation/examples/param_sweep.py`
```python
import pandas as pd
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from documentation.examples import param_sweep
from cadCAD import configs

exec_mode = ExecutionMode()
local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_mode_ctx, configs=configs)

raw_result, tensor_field, sessions = run.execute()
result = pd.DataFrame(raw_result)
print()
print("Tensor Field:")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
```
