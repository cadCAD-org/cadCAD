from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim

# last_partial_state_update_block
def last_update_block(_g, substep, sH, s, _input):
    return 'sh', sH[-1]


# Policies per Mechanism
def p(_g, substep, sH, s):
    return {'last_update_block': sH[-1]}

def add(y, x):
    return lambda _g, substep, sH, s, _input: (y, s[y] + x)

def policies(_g, substep, sH, s, _input):
    y = 'policies'
    x = _input
    return (y, x)

policies = {"p1": p, "p2": p}

genesis_states = {
    's': 0,
    'sh': [{}], # {[], {}}
    # 'policies': {},
}

variables = {
    's': add('s', 1),
    'sh': last_update_block,
    # "policies": policies
}


PSUB = {
    "policies": policies,
    "variables": variables
}

partial_state_update_block = {
    "PSUB1": PSUB,
    "PSUB2": PSUB,
    "PSUB3": PSUB
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
    seeds={},
    raw_exogenous_states={},
    env_processes={},
    partial_state_update_blocks=partial_state_update_block,
    policy_ops=[lambda a, b: a + b]
)
