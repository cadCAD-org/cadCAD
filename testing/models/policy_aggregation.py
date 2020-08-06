from cadCAD.configuration.utils import config_sim


# Policies per Mechanism
from testing.experiments import exp_policy_agg


def p1m1(_g, step, sL, s, **kwargs):
    return {'policy1': 1}
def p2m1(_g, step, sL, s, **kwargs):
    return {'policy2': 2}

def p1m2(_g, step, sL, s, **kwargs):
    return {'policy1': 2, 'policy2': 2}
def p2m2(_g, step, sL, s, **kwargs):
    return {'policy1': 2, 'policy2': 2}

def p1m3(_g, step, sL, s, **kwargs):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}
def p2m3(_g, step, sL, s, **kwargs):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}


# Internal States per Mechanism
def add(y, x):
    return lambda _g, step, sH, s, _input, **kwargs: (y, s[y] + x)

def policies(_g, step, sH, s, _input, **kwargs):
    y = 'policies'
    x = _input
    return (y, x)


# Genesis States
genesis_states = {
    'policies': {},
    's1': 0
}

variables = {
    's1': add('s1', 1),
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


exp_policy_agg.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=partial_state_update_block,
    policy_ops=[lambda a, b: a + b, lambda y: y * 2] # Default: lambda a, b: a + b
)
