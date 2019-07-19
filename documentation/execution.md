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
    * **Single Process:** A single process Execution Mode for a single System Model Configuration (Example: 
    `cadCAD.engine.ExecutionMode().single_proc`).
    * **Multi-Process:** Multiple process Execution Mode for System Model Simulations which executes on a thread per 
    given System Model Configuration (Example: `cadCAD.engine.ExecutionMode().multi_proc`).
2. #### *Create Execution Context using Execution Mode:*
```python
from cadCAD.engine import ExecutionMode, ExecutionContext
exec_mode = ExecutionMode()
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
```
3. #### *Create Simulation Executor*
```python
from cadCAD.engine import Executor
from cadCAD import configs
simulation = Executor(exec_context=single_proc_ctx, configs=configs)
```
4. #### *Execute Simulation: Produce System Event Dataset*
A Simulation execution produces a System Event Dataset and the Tensor Field applied to initial states used to create it. 
```python
import pandas as pd
raw_system_events, tensor_field = simulation.execute()

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
```python
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

##### [Single Process Example Execution](link)

##### [Multiple Process Example Execution](link)
