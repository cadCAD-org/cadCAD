import pandas as pd
from tabulate import tabulate

from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.configuration import Experiment
from cadCAD import configs

# Policies per Mechanism
def p1m1(_g, step, sH, s):
    return {'policy1': 1}
def p2m1(_g, step, sH, s):
    return {'policy2': 2}

def p1m2(_g, step, sH, s):
    return {'policy1': 2, 'policy2': 2}
def p2m2(_g, step, sH, s):
    return {'policy1': 2, 'policy2': 2}

def p1m3(_g, step, sH, s):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}
def p2m3(_g, step, sH, s):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}


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
    's1': 0
}

variables = {
    's1': add('s1', 1),
    "policies": policies
}

psubs = {
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

exp = Experiment()
exp.append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    partial_state_update_blocks=psubs,
    policy_ops=[lambda a, b: a + b, lambda y: y * 2] # Default: lambda a, b: a + b
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
