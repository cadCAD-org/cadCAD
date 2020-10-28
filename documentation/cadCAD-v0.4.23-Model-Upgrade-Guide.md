<table>
    <tr>
        <th>
            Feature
        </th>
        <th>
            ver. 0.4.23
        </th>
      <th>
            ver. 0.3.1 (Deprecated)
        </th>
    </tr>
    <tr>
        <td>
           <h5>
                Experiments
            </h5>
        </td>
        <td>
<pre lang="python">
from cadCAD.configuration import Experiment
exp = Experiment()
exp.append_configs(...) 
</pre>
        </td>
        <td>
<pre lang="python">
from cadCAD.configuration import append_configs
append_configs(…)         
</pre>
        </td>
</tr>
<tr>
        <td>
           <h5>
                Local Execution Mode
            </h5>
        </td>
        <td>
<pre lang="python">          
from cadCAD.engine import ExecutionMode, ExecutionContext
exec_mode = ExecutionMode()
local_ctx = ExecutionContext(context=exec_mode.local_mode)         
</pre>
        </td>
        <td>
         <p>Multi-Threaded</p>
         <pre lang="python">
from cadCAD.engine import ExecutionMode, ExecutionContext
exec_mode = ExecutionMode()
single_ctx = ExecutionContext(context=exec_mode.multi_proc)
</pre>
<p>Single-Threaded</p>
<pre lang="python">
from cadCAD.engine import ExecutionMode, ExecutionContext
exec_mode = ExecutionMode()
multi_ctx = ExecutionContext(context=exec_mode.single_proc)
            </pre>
        </td>
   </tr>
 <tr>
        <td>
           <h5>
                cadCAD Post-Processing Enhancements / Modifications
           </h5>
        </td>
        <td>
            <pre lang="python">
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
import system_model_A, system_model_B

from cadCAD import configs
exec_mode = ExecutionMode()

local_ctx = ExecutionContext(context=exec_mode.local_mode)
simulation = Executor(exec_context=local_ctx, configs=configs)
raw_result, sys_model, _ = simulation.execute()
result = pd.DataFrame(raw_result)
print(tabulate(result, headers='keys', tablefmt='psql'))
</pre>
        </td>
        <td>
         <pre lang="python">
        
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
import system_model_A, system_model_B
from cadCAD import configs

exec_mode = ExecutionMode()
multi_ctx = ExecutionContext(context=exec_mode.multi_proc)
simulation = Executor(exec_context=multi_ctx, configs=configs)
i = 0
config_names = ['sys_model_A', 'sys_model_B']
for raw_result, _ in simulation.execute():
result = pd.DataFrame(raw_result)
print()
print(f"{config_names[i]} Result: System Events DataFrame:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
i += 1
           
   </pre>
        </td>
   </tr>

 <tr>
        <td>
           <h5>
             Expandable state and policy update parameter
            </h5>
        </td>
        <td>
            <pre lang="python">
def state_update(_params, substep, sH, s, _input, **kwargs):
…
return 'state_variable_name', new_value
def policy(_params, substep, sH, s, **kwargs):
…
return {'signal_1': value_1, …, 'signal_N': value_N}
   </pre>
        </td>
        <td>
         <pre lang="python">     
def state_update(_params, substep, sH, s, _input):
…
return 'state_variable_name', new_value
def policy(_params, substep, sH, s):
…
return {'signal_1': value_1, …, 'signal_N': value_N}  
   </pre>
        </td>
   </tr>
</table>
