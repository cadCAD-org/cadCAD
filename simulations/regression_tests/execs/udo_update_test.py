from pprint import pprint
import pandas as pd
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import udo_inter_substep_update
from cadCAD import configs

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

raw_result, tensor_fields, sessions = run.execute()
# cols = configs[0].initial_state.keys()
cols = [
    'increment',
    'state_udo_tracker_a', 'state_udo', 'state_udo_perception_tracker', 'state_udo_tracker_b',
    'udo_policy_tracker_a', 'udo_policies', 'udo_policy_tracker_b',
    'timestamp'
]
result = pd.DataFrame(raw_result)[['run', 'substep', 'timestep'] + cols]
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
pprint(sessions)
print(tabulate(result, headers='keys', tablefmt='psql'))
