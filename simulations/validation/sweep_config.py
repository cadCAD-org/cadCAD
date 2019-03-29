from decimal import Decimal
import numpy as np
from datetime import timedelta
import pprint

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import proc_trigger, ep_time_step, config_sim

from typing import Dict, List

pp = pprint.PrettyPrinter(indent=4)

seeds = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}


g: Dict[str, List[int]] = {
    'alpha': [1],
    'beta': [2, 5],
    'gamma': [3, 4],
    'omega': [7]
}

# Policies per Mechanism
def p1m1(_g, step, sL, s):
    return {'param1': 1}

def p2m1(_g, step, sL, s):
    return {'param2': 4}

def p1m2(_g, step, sL, s):
    return {'param1': 'a', 'param2': _g['beta']}

def p2m2(_g, step, sL, s):
    return {'param1': 'b', 'param2': 0}

def p1m3(_g, step, sL, s):
    return {'param1': np.array([10, 100])}

def p2m3(_g, step, sL, s):
    return {'param1': np.array([20, 200])}

# Internal States per Mechanism
def s1m1(_g, step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)

def s2m1(_g, step, sL, s, _input):
    y = 's2'
    x = _g['beta']
    return (y, x)

def s1m2(_g, step, sL, s, _input):
    y = 's1'
    x = _input['param2']
    return (y, x)

def s2m2(_g, step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m3(_g, step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)

def s2m3(_g, step, sL, s, _input):
    y = 's2'
    x = 0
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3


def es3p1(_g, step, sL, s, _input):
    y = 's3'
    x = _g['gamma']
    return (y, x)
# @curried
def es4p2(_g, step, sL, s, _input):
    y = 's4'
    x = _g['gamma']
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
def es5p2(_g, step, sL, s, _input):
    y = 'timestep'
    x = ep_time_step(s, dt_str=s['timestep'], fromat_str=ts_format, _timedelta=t_delta)
    return (y, x)


# Environment States
# @curried
# def env_a(param, x):
#     return x + param
def env_a(x):
    return x
def env_b(x):
    return 10


# Genesis States
genesis_states = {
    's1': Decimal(0.0),
    's2': Decimal(0.0),
    's3': Decimal(1.0),
    's4': Decimal(1.0),
#     'timestep': '2018-10-01 15:16:24'
}


# remove `exo_update_per_ts` to update every ts
raw_exogenous_states = {
    "s3": es3p1,
    "s4": es4p2,
#     "timestep": es5p2
}


# ToDo: make env proc trigger field agnostic
# ToDo: input json into function renaming __name__
triggered_env_b = proc_trigger(1, env_b)
env_processes = {
    "s3": env_a, #sweep(beta, env_a),
    "s4": triggered_env_b #rename('parameterized', triggered_env_b) #sweep(beta, triggered_env_b)
}
# parameterized_env_processes = parameterize_states(env_processes)
#
# pp.pprint(parameterized_env_processes)
# exit()

# ToDo: The number of values entered in sweep should be the # of config objs created,
# not dependent on the # of times the sweep is applied
# sweep exo_state func and point to exo-state in every other funtion
# param sweep on genesis states

partial_state_update_block = {
    "m1": {
        "policies": {
            "b1": p1m1,
            "b2": p2m1
        },
        "variables": {
            "s1": s1m1,
            "s2": s2m1
        }
    },
    "m2": {
        "policies": {
            "b1": p1m2,
            "b2": p2m2,
        },
        "variables": {
            "s1": s1m2,
            "s2": s2m2
        }
    },
    "m3": {
        "policies": {
            "b1": p1m3,
            "b2": p2m3
        },
        "variables": {
            "s1": s1m3,
            "s2": s2m3
        }
    }
}


sim_config = config_sim(
    {
        "N": 2,
        "T": range(5),
        "M": g
    }
)


append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    seeds=seeds,
    raw_exogenous_states=raw_exogenous_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_block
)