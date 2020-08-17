import pprint
from typing import Dict, List

import pandas as pd
from tabulate import tabulate

from cadCAD.configuration.utils import env_trigger, var_substep_trigger, config_sim, psub_list
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs

pp = pprint.PrettyPrinter(indent=4)


def some_function(x):
    return x


g: Dict[str, List[int]] = {
    'alpha': [1],
    'beta': [2, 5],
    'gamma': [3, 4],
    'omega': [some_function]
}

psu_steps = ['1', '2', '3']
system_substeps = len(psu_steps)
var_timestep_trigger = var_substep_trigger([0, system_substeps])
env_timestep_trigger = env_trigger(system_substeps)
env_process = {}


# Policies
def gamma(_params, step, sH, s):
    return {'gamma': _params['gamma']}


def omega(_params, step, sH, s):
    return {'omega': _params['omega'](7)}


# Internal States
def alpha(_params, step, sH, s, _input):
    return 'alpha', _params['alpha']

def alpha_plus_gamma(_params, step, sH, s, _input):
    return 'alpha_plus_gamma', _params['alpha'] + _params['gamma']


def beta(_params, step, sH, s, _input):
    return 'beta', _params['beta']


def policies(_params, step, sH, s, _input):
    return 'policies', _input


def sweeped(_params, step, sH, s, _input):
    return 'sweeped', {'beta': _params['beta'], 'gamma': _params['gamma']}


genesis_states = {
    'alpha_plus_gamma': 0,
    'alpha': 0,
    'beta': 0,
    'policies': {},
    'sweeped': {}
}

env_process['sweeped'] = env_timestep_trigger(trigger_field='timestep', trigger_vals=[5], funct_list=[lambda _g, x: _g['beta']])

sim_config = config_sim(
    {
        "N": 2,
        "T": range(5),
        "M": g,
    }
)

psu_block = {k: {"policies": {}, "variables": {}} for k in psu_steps}
for m in psu_steps:
    psu_block[m]['policies']['gamma'] = gamma
    psu_block[m]['policies']['omega'] = omega
    psu_block[m]["variables"]['alpha'] = alpha_plus_gamma
    psu_block[m]["variables"]['alpha_plus_gamma'] = alpha
    psu_block[m]["variables"]['beta'] = beta
    psu_block[m]['variables']['policies'] = policies
    psu_block[m]["variables"]['sweeped'] = var_timestep_trigger(y='sweeped', f=sweeped)

psubs = psub_list(psu_block, psu_steps)
print()
pp.pprint(psu_block)
print()

exp = Experiment()
exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    env_processes=env_process,
    partial_state_update_blocks=psubs
)

exec_mode = ExecutionMode()
local_proc_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=local_proc_ctx, configs=configs)

raw_result, tensor_field, sessions = run.execute()
result = pd.DataFrame(raw_result)
print()
print("Tensor Field:")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()