from decimal import Decimal

import numpy as np

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import bound_norm_random, config_sim

seeds = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}


# Policies per Mechanism
def p1(_g, step, sL, s):
    return {'param1': 10}
def p2(_g, step, sL, s):
    return {'param1': 10, 'param2': 40}


# Internal States per Mechanism
def s1(_g, step, sL, s, _input):
    y = 'ds1'
    x = s['ds1'] + 1
    return (y, x)
def s2(_g, step, sL, s, _input):
    y = 'ds2'
    x = _input['param2']
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3

def es(_g, step, sL, s, _input):
    y = 'ds3'
    x = s['ds3'] * bound_norm_random(seeds['a'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)


# Environment States
def env_a(x):
    return 5
def env_b(x):
    return 10


# Genesis States
genesis_states = {
    'ds1': Decimal(0.0),
    'ds2': Decimal(0.0),
    'ds3': Decimal(1.0)
}


raw_exogenous_states = {
    "ds3": es
}


env_processes = {
    "ds3": env_a
}


partial_state_update_block = {
    "m1": {
        "policies": {
            "p1": p1,
            "p2": p2
        },
        "variables": {
            "ds1": s1,
            "ds2": s2
        }
    },
    "m2": {
        "policies": {
            "p1": p1,
            "p2": p2
        },
        "variables": {
            "ds1": s1,
            "ds2": s2
        }
    },
    "m3": {
        "policies": {
            "p1": p1,
            "p2": p2
        },
        "variables": {
            "ds1": s1,
            "ds2": s2
        }
    }
}


sim_config = config_sim(
    {
        "N": 2,
        "T": range(4),
    }
)

append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    seeds=seeds,
    raw_exogenous_states=raw_exogenous_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_block,
    policy_ops=[lambda a, b: a + b]
)