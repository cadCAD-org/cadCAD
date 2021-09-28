<table>
    <tr>
        <th>
            Feature
        </th>
        <th>
            ver. 0.4.28
        </th>
        <th>
            ver. 0.4.23
        </th>
    </tr>
    <tr>
        <td>
           <h5>
                Experiments & System Model Configurations
            </h5>
        </td>
        <td>
<pre lang="python">
from cadCAD.configuration import Experiment

exp = Experiment()
exp.append_model(
    model_id = 'sys_model_1', # System Model
    initial_state = ..., # System Model
    partial_state_update_blocks = ..., # System Model
    policy_ops = ..., # System Model
    sim_configs = ..., # Simulation Properties
)
exp.append_model(...)

configs = exp.configs
</pre>
        </td>
        <td>
<pre lang="python">
from cadCAD import configs
from cadCAD.configuration import Experiment
exp = Experiment()
exp.append_configs(...)       
</pre>
        </td>
</tr>
 <tr>
        <td>
           <h5>
                cadCAD Post-Processing Modifications
           </h5>
        </td>
        <td>
            <pre lang="python">
import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.experiments import multi_exp
from simulations.regression_tests.models import config_multi_1, config_multi_2

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=multi_exp.configs)

raw_result, tensor_fields, _ = run.execute()
result = pd.DataFrame(raw_result)
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
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

local_ctx = ExecutionContext(context=exec_mode.local_mode)
simulation = Executor(exec_context=local_ctx, configs=configs)
raw_result, sys_model, _ = simulation.execute()
result = pd.DataFrame(raw_result)
print(tabulate(result, headers='keys', tablefmt='psql'))           
   </pre>
        </td>
   </tr>
</table>
