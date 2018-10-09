from engine.utils import bound_norm_random, ep_time_step, env_proc

import numpy as np
from decimal import Decimal

seed = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}

# Behaviors per Mechanism
def b1m1(step, sL, s):
    return s['s1'] + 1
def b2m1(step, sL, s):
    return s['s1'] + 1

def b1m2(step, sL, s):
    return s['s1'] + 1
def b2m2(step, sL, s):
    return s['s1'] + 1

def b1m3(step, sL, s):
    return s['s1'] + 1
def b2m3(step, sL, s):
    return s['s2'] + 1


# Internal States per Mechanism
def s1m1(step, sL, s, _input):
    s['s1'] = s['s1'] + _input
def s2m1(step, sL, s, _input):
    s['s2'] = s['s2'] + _input


def s1m2(step, sL, s, _input):
    s['s1'] = s['s1'] + _input
def s2m2(step, sL, s, _input):
    s['s2'] = s['s2'] + _input

def s1m3(step, sL, s, _input):
    s['s1'] = s['s1'] + _input
def s2m3(step, sL, s, _input):
    s['s2'] = s['s2'] + _input

# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3
def es3p1(step, sL, s, _input):
    s['s3'] = s['s3'] * bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
def es4p2(step, sL, s, _input):
    s['s4'] = s['s4'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B)
def es5p2(step, sL, s, _input):
    s['timestamp'] = ep_time_step(s, s['timestamp'], seconds=1)

# Environment States
def env_a(x):
    return x
def env_b(x):
    return x
def what_ever(x):
    return x + 1

# Genesis States
state_dict = {
    's1': Decimal(0.0),
    's2': Decimal(0.0),
    's3': Decimal(1.0),
    's4': Decimal(1.0),
    'timestamp': '2018-10-01 15:16:24'
}

exogenous_states = {
    "s3": es3p1,
    "s4": es4p2,
    "timestamp": es5p2
}

env_processes = {
    "s3": env_proc('2018-10-01 15:16:25', env_a),
    "s4": env_proc('2018-10-01 15:16:25', env_b)
}

mechanisms = {
    "m1": {
        "behaviors": {
            "b1": b1m1,
            "b2": b2m1
        },
        "states": {
            "s1": s1m1,
            "s2": s2m1,
        }
    },
    "m2": {
        "behaviors": {
            "b1": b1m2,
            "b2": b2m2
        },
        "states": {
            "s1": s1m2,
            "s2": s2m2,
        }
    },
    "m3": {
        "behaviors": {
            "b1": b1m3,
            "b2": b2m3
        },
        "states": {
            "s1": s1m3,
            "s2": s2m3,
        }
    }
}

sim_config = {
    "N": 2
}