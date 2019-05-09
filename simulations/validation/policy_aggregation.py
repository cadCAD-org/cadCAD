import numpy as np
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim

# ToDo: Use
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

def p1m2(_g, step, sL, s):
    return {'param1': 2, 'param2': 2}
def p2m2(_g, step, sL, s):
    return {'param1': 2, 'param2': 2}

def p1m3(_g, step, sL, s):
    return {'param1': 1, 'param2': 2, 'param3': 3}
def p2m3(_g, step, sL, s):
    return {'param1': 1, 'param2': 2, 'param3': 3}


# Internal States per Mechanism
def add(y, x):
    return lambda _g, step, sH, s, _input: (y, s[y] + x)

def policies(_g, step, sH, s, _input):
    y = 'policies'
    x = _input
    return (y, x)

# Genesis States
genesis_states = {
    'policies': {},
    's1': 0,
    's2': 0,
}

raw_exogenous_states = {}

env_processes = {}

variables = {
    's1': add('s1', 1),
    's2': add('s2', 1),
    "policies": policies
}

partial_state_update_block = {
    "m1": {
        "policies": {
            "p1": p1m1,
            "p2": p2m1
        },
        "variables": variables
    },
    "m2": {
        "policies": {
            "p1": p1m2,
            "p2": p2m2
        },
        "variables": variables
    },
    "m3": {
        "policies": {
            "p1": p1m3,
            "p2": p2m3
        },
        "variables": variables
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
    policy_ops=[lambda a, b: a + b, lambda y: y + 10, lambda y: y + 30]
)