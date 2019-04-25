from decimal import Decimal
from functools import reduce

import numpy as np
from datetime import timedelta

from cadCAD.configuration.utils.policyAggregation import get_base_value

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import proc_trigger, bound_norm_random, ep_time_step, config_sim

seeds = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}


# Policies per Mechanism
def p1m1(_g, step, sL, s):
    return {'param1': 1}
def p2m1(_g, step, sL, s):
    return {'param2': 2}

# []

def p1m2(_g, step, sL, s):
    return {'param1': 2, 'param2': 2}
def p2m2(_g, step, sL, s):
    return {'param1': 2, 'param2': 2}

def p1m3(_g, step, sL, s):
    return {'param1': 1, 'param2': 2, 'param3': 3}
def p2m3(_g, step, sL, s):
    return {'param1': 1, 'param2': 2, 'param3': 3}

def test_pipeline(_g, step, sL, s):
    return {'test': 2, 'param2': 2}


# Internal States per Mechanism
def s(y):
    return lambda _g, step, sH, s, _input: (y, s[y] + 1)

def sH(_g, step, sH, s, _input):
    y = 'sh'
    x = sH
    return (y, x)

def policies(_g, step, sH, s, _input):
    y = 'policies'
    x = _input
    return (y, x)

# Genesis States
genesis_states = {
    'policies': {},
    's1': 0,
    's2': 0,
    # 'sh': []
}

raw_exogenous_states = {}

env_processes = {}

partial_state_update_block = {
    "m1": {
        "policies": {
            "b1": p1m1,
            "b2": p2m1
        },
        "variables": {
            's1': s('s1'),
            's2': s('s2'),
            # 'sh': sH,
            "policies": policies
        }
    },
    "m2": {
        "policies": {
            "b1": p1m2,
            "b2": p2m2
        },
        "variables": {
            's1': s('s1'),
            's2': s('s2'),
            # 'sh': sH,
            "policies": policies
        }
    },
    "m3": {
        "policies": {
            "b1": p1m3,
            "b2": p2m3
        },
        "variables": {
            's1': s('s1'),
            's2': s('s2'),
            # 'sh': sH,
            "policies": policies
        }
    }
}


sim_config = config_sim(
    {
        "N": 1,
        "T": range(3),
    }
)


append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    seeds=seeds,
    raw_exogenous_states=raw_exogenous_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_block,
    # policy_ops=[lambda a, b: a + b, lambda y: y + 100, lambda y: y + 300]
)


# def p1m3(_g, step, sL, s):
#     return {'param1': 1, 'param2': 2, 'param3': 3}
# def p2m3(_g, step, sL, s):
#     return {'param1': 1, 'param2': 2, 'param3': 3}
#
# xx = {'param1': [1,1], 'param2': [2,2], 'param3': [3,3]}