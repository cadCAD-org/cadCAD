import json, pathlib, pandas as pd

from cadCAD import configs
from cadCAD.configuration import Experiment
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.models import param_sweep, policy_aggregation


del configs[:]
exp = Experiment()
sys_model_A_id = "sys_model_A"
exp.append_configs(
    sim_configs=param_sweep.sim_config,
    initial_state=param_sweep.genesis_states,
    env_processes=param_sweep.env_process,
    partial_state_update_blocks=param_sweep.partial_state_update_blocks
)
sys_model_B_id = "sys_model_B"
exp.append_configs(
    sim_configs=param_sweep.sim_config,
    initial_state=param_sweep.genesis_states,
    env_processes=param_sweep.env_process,
    partial_state_update_blocks=param_sweep.partial_state_update_blocks
)
sys_model_C_id = "sys_model_C"
exp.append_configs(
    sim_configs=policy_aggregation.sim_config,
    initial_state=policy_aggregation.genesis_states,
    partial_state_update_blocks=policy_aggregation.partial_state_update_block,
    policy_ops=[lambda a, b: a + b, lambda y: y * 2] # Default: lambda a, b: a + b
)

exec_mode = ExecutionMode()
local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
simulation = Executor(exec_context=local_mode_ctx, configs=configs)
raw_results, _, _ = simulation.execute()

results_df = pd.DataFrame(raw_results)
result_rows = len(results_df.index)

file_dir = pathlib.Path(__file__).parent.absolute()
file_path = f'{file_dir}/0_4_23_record_count.json'
with open(file_path, 'w') as json_file:
    record_count = {'record_count': result_rows}
    json.dump(record_count, json_file)
