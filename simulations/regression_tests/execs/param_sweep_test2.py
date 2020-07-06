from pprint import pprint

import pandas as pd
from tabulate import tabulate
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.configuration.utils import configs_as_objs
from simulations.regression_tests.models import sweep_config
from cadCAD import configs

exec_mode = ExecutionMode()

local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)
#
raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
print(result.head(10))
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
# print(tabulate(result.head(), headers='keys', tablefmt='psql'))

a = configs
b = configs_as_objs(configs)

for config in configs:
    print()
    # pprint(config.__dict__)
    print('simulation_id: '+ str(config.__dict__['simulation_id']))
    print('run_id: '+ str(config.__dict__['run_id']))
    print('N: ' + str(config.__dict__['sim_config']['N']))
    # print('M: ' + str(config.__dict__['sim_config']['M']))
    # print('sim_config:')
    # pprint(config.__dict__['sim_config'])
    # print()

# pprint(a)
# print()
# print()
# pprint(b[0].sim_config)
# pprint(b[0]['sim_config'])

configs
configs = configs_as_objs(configs)


# {'run_id': 0,
#   'session_id': 'cadCAD_user=0_0',
#   'simulation_id': 0,
#   'user_id': 'cadCAD_user'
#  }