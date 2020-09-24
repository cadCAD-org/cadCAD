from pprint import pprint
import pandas as pd
from tabulate import tabulate

from cadCAD import remote_dict
sys_job_metrics = {'sim_id': 2, 'subset_id': 0, 'run': 2}
remote_dict['metrics'] = sys_job_metrics

from simulations.regression_tests.models import config_multi_1, config_multi_2
from simulations.regression_tests.experiments import multi_exp
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

print(multi_exp.ser_flattened_configs)
print()
for c in multi_exp.configs:
    print('-' * 20)
    # print(f"exp_run_id          : {c.__dict__['exp_run_id']}")
    print(f"experiment_id       : {c.__dict__['experiment_id']}")
    print(f"  * user_id         : {c.__dict__['user_id']}")
    print(f"  * exp_creation_ts : {c.__dict__['exp_creation_ts']}")
    # print(f"  * config_creation_ts : {c.__dict__['config_creation_ts']}")
    print()
    print("System Metrics:")
    print(f"simulation_id       : {c.__dict__['simulation_id']}")
    print(f"subset_id           : {c.__dict__['subset_id']}")
    print(f"run_id              : {c.__dict__['run_id']}")
    print()
print()

# pprint(len(multi_exp.original_configs))
# pprint(multi_exp.original_configs)
# print()
# pprint(len(multi_exp.ser_flattened_configs))
# # pprint(self.ser_flattened_configs)
# print()
# pprint(len(multi_exp.flattened_configs))
# pprint(multi_exp.flattened_configs)
# print()
# exit()

exec_mode = ExecutionMode()
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=multi_exp.configs, empty_return=False)

raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
print(tabulate(result, headers='keys', tablefmt='psql'))