from functools import reduce
from pprint import pprint

import pandas as pd
from tabulate import tabulate

from cadCAD.configuration.utils import configs_as_dicts, configs_as_objs #, configs_as_spec
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import sweep_config
from cadCAD import configs

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

# raw_result, tensor_fields, sessions = run.execute()
# result = pd.DataFrame(raw_result)
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
# print(tabulate(result, headers='keys', tablefmt='psql'))

# print()
# print(len(configs_as_dicts(configs)))
# print(len(configs_as_spec(configs)))
# pprint(configs_as_spec(configs))
# pprint(configs_as_dicts(configs))
# for d in configs_as_dicts(configs):
#     print(d['env_processes'])

ds = configs_as_dicts(configs)
ds2 = configs_as_objs(configs)
for c in ds2:
    print(c.__dict__)
    print()
exit()
# print(ds2)
# exit()
# pprint(ds)

# [for x in d]

# exogenous_states = lambda x, y: ()
# fd = {
#     'exogenous_states': lambda x, y: ('exogenous_states', list(set([x['exogenous_states'], y['exogenous_states']]))),
#     'exp_window': lambda x, y: ('exp_window', list(set([x['exp_window'], y['exp_window']])))
# }
# fd['exogenous_states'](x, y)
# new_d = dict([reduce(lambda x, y: [x, y], ds)])
# print(new_d)
# exit()


new_d = dict(reduce(lambda x, y: list(zip(x.keys(), zip(x.values(), y.values()))), ds))
# new_d
# new_d.items()

# def format_config_val(x):
#     if type(x) is dict:

cast_list = lambda k, v: (k, list(v))
unique_values = lambda k, v: (k, list(set(list(v))))
select_dict = lambda k, v: (k, v[0])
fd = {
    'env_processes': select_dict,
    'exogenous_states': unique_values,
    'exp_window': unique_values,
    'experiment_id': unique_values,
    'initial_state': unique_values,
    'kwargs': cast_list,
    'partial_state_updates': cast_list,
    'policy_ops': unique_values,
    'run_id': unique_values
}

# f = [t[1]list(t[1]) for t in new_d.items()]
# f = [fd[k](k, ) for k, v in new_d.items()]
pprint(new_d)
exit()

pprint([d['exogenous_states'] for d in ds])
print()

pprint([d['exp_window'] for d in ds])
print()

vv = [d['experiment_id'] for d in ds]
pprint(vv)
print()

# pprint([d['initial_state'] for d in ds])
# print()

# pprint([d['kwargs'] for d in ds])
# print()

# pprint([d['partial_state_updates'] for d in ds])
# print()

# pprint([d['policy_ops'] for d in ds])
# print()

# pprint([d['run_id'] for d in ds])
# print()

# pprint([d['seeds'] for d in ds])
# print()

# pprint([d['session_id'] for d in ds])
# print()

# pprint([d['sim_config'] for d in ds])
# print()

# pprint([d['simulation_id'] for d in ds])
# print()

# pprint([d['subset_id'] for d in ds])
# print()

# pprint([d['subset_window'] for d in ds])
# print()

pprint([d['user_id'] for d in ds])
print()

# print()