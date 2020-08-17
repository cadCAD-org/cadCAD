import numpy as np
from datetime import timedelta
import pprint

from cadCAD.configuration.utils import env_trigger, var_substep_trigger, config_sim, time_step, psub_list

from typing import Dict, List

from simulations.regression_tests.experiments import sweep_exp

pp = pprint.PrettyPrinter(indent=4)

seeds = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}

# Optional
g: Dict[str, List[int]] = {
    'alpha': [1],
    # 'beta': [2],
    # 'gamma': [3],
    'beta': [2, 5],
    'gamma': [3, 4],
    'omega': [7]
}

psu_steps = ['m1', 'm2', 'm3']
system_substeps = len(psu_steps)
var_timestep_trigger = var_substep_trigger([0, system_substeps])
env_timestep_trigger = env_trigger(system_substeps)
env_process = {}
psu_block = {k: {"policies": {}, "variables": {}} for k in psu_steps}

# ['s1', 's2', 's3', 's4']
# Policies per Mechanism
def p1m1(_g, step, sL, s, **kwargs):
    return {'param1': 1}
psu_block['m1']['policies']['p1'] = p1m1

def p2m1(_g, step, sL, s, **kwargs):
    return {'param2': 4}
psu_block['m1']['policies']['p2'] = p2m1

def p1m2(_g, step, sL, s, **kwargs):
    return {'param1': 'a', 'param2': _g['beta']}
psu_block['m2']['policies']['p1'] = p1m2

def p2m2(_g, step, sL, s, **kwargs):
    return {'param1': 'b', 'param2': 0}
psu_block['m2']['policies']['p2'] = p2m2

def p1m3(_g, step, sL, s, **kwargs):
    return {'param1': np.array([10, 100])}
psu_block['m3']['policies']['p1'] = p1m3

def p2m3(_g, step, sL, s, **kwargs):
    return {'param1': np.array([20, 200])}
psu_block['m3']['policies']['p2'] = p2m3


# Internal States per Mechanism
def s1m1(_g, step, sL, s, _input, **kwargs):
    return 's1', 0
psu_block['m1']["variables"]['s1'] = s1m1

def s2m1(_g, step, sL, s, _input, **kwargs):
    return 's2', _g['beta']
psu_block['m1']["variables"]['s2'] = s2m1

def s1m2(_g, step, sL, s, _input, **kwargs):
    return 's1', _input['param2']
psu_block['m2']["variables"]['s1'] = s1m2

def s2m2(_g, step, sL, s, _input, **kwargs):
    return 's2', _input['param2']
psu_block['m2']["variables"]['s2'] = s2m2

def s1m3(_g, step, sL, s, _input, **kwargs):
    return 's1', 0
psu_block['m3']["variables"]['s1'] = s1m3

def s2m3(_g, step, sL, s, _input, **kwargs):
    return 's2', 0
psu_block['m3']["variables"]['s2'] = s2m3


# Exogenous States
def update_timestamp(_g, step, sL, s, _input, **kwargs):
    y = 'timestamp'
    return y, time_step(dt_str=s[y], dt_format='%Y-%m-%d %H:%M:%S', _timedelta=timedelta(days=0, minutes=0, seconds=1))
for m in ['m1','m2','m3']:
    # psu_block[m]["variables"]['timestamp'] = update_timestamp
    psu_block[m]["variables"]['timestamp'] = var_timestep_trigger(y='timestamp', f=update_timestamp)
    # psu_block[m]["variables"]['timestamp'] = var_trigger(
    #     y='timestamp', f=update_timestamp, pre_conditions={'substep': [0, system_substeps]}, cond_op=lambda a, b: a and b
    # )

proc_one_coef = 0.7
def es3(_g, step, sL, s, _input, **kwargs):
    return 's3', s['s3'] + proc_one_coef
# use `timestep_trigger` to update every ts
for m in ['m1','m2','m3']:
    psu_block[m]["variables"]['s3'] = var_timestep_trigger(y='s3', f=es3)


def es4(_g, step, sL, s, _input, **kwargs):
    return 's4', s['s4'] + _g['gamma']
for m in ['m1','m2','m3']:
    psu_block[m]["variables"]['s4'] = var_timestep_trigger(y='s4', f=es4)

# Genesis States
genesis_states = {
    's1': 0.0,
    's2': 0.0,
    's3': 1.0,
    's4': 1.0,
    'timestamp': '2018-10-01 15:16:24'
}


# Environment Process
env_process["s3"] = [lambda _g, x: _g['beta'], lambda _g, x: x + 1]
env_process["s4"] = env_timestep_trigger(trigger_field='timestep', trigger_vals=[5], funct_list=[lambda _g, x: _g['beta']])


# config_sim Necessary
sim_config = config_sim(
    {
        "N": 5,
        "T": range(2),
        "M": g, # Optional
    }
)

# New Convention
partial_state_update_blocks = psub_list(psu_block, psu_steps)
sweep_exp.append_configs(
    # user_id='user_a',
    sim_configs=sim_config,
    initial_state=genesis_states,
    seeds=seeds,
    env_processes=env_process,
    partial_state_update_blocks=partial_state_update_blocks
)


# print()
# print("Partial State Update Block:")
# pp.pprint(partial_state_update_blocks)
# print()
# print()
