from decimal import Decimal
import numpy as np
from datetime import timedelta

from SimCAD import configs
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step


seed = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}


# Behaviors per Mechanism
def b1m1(step, sL, s):
    return {'param1': 1}
def b2m1(step, sL, s):
    return {'param2': 4}

def b1m2(step, sL, s):
    return {'param1': 'a', 'param2': 2}
def b2m2(step, sL, s):
    return {'param1': 'b', 'param2': 4}

def b1m3(step, sL, s):
    return {'param1': ['c'], 'param2': np.array([10, 100])}
def b2m3(step, sL, s):
    return {'param1': ['d'], 'param2': np.array([20, 200])}


# Internal States per Mechanism
def s1m1(step, sL, s, _input):
    y = 's1'
    x = _input['param1']
    return (y, x)
def s2m1(step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m2(step, sL, s, _input):
    y = 's1'
    x = _input['param1']
    return (y, x)
def s2m2(step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m3(step, sL, s, _input):
    y = 's1'
    x = _input['param1']
    return (y, x)
def s2m3(step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3

def es3p1(step, sL, s, _input):
    y = 's3'
    x = s['s3'] * bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

def es4p2(step, sL, s, _input):
    y = 's4'
    x = s['s4'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
def es5p2(step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=t_delta)
    return (y, x)


# Environment States
def env_a(x):
    return 5
def env_b(x):
    return 10
# def what_ever(x):
#     return x + 1


# Genesis States
genesis_states = {
    's1': Decimal(0.0),
    's2': Decimal(0.0),
    's3': Decimal(1.0),
    's4': Decimal(1.0),
    'timestamp': '2018-10-01 15:16:24'
}


# remove `exo_update_per_ts` to update every ts
exogenous_states = exo_update_per_ts(
    {
    "s3": es3p1,
    "s4": es4p2,
    "timestamp": es5p2
    }
)


env_processes = {
    "s3": env_a,
    "s4": proc_trigger('2018-10-01 15:16:25', env_b)
}


mechanisms = {
    "m1": {
        "behaviors": {
            "b1": b1m1,
            "b2": b2m1
        },
        "states": {
            "s1": s1m1,
            "s2": s2m1
        }
    },
    "m2": {
        "behaviors": {
            "b1": b1m2,
            "b2": b2m2
        },
        "states": {
            "s1": s1m2,
            "s2": s2m2
        }
    },
    "m3": {
        "behaviors": {
            "b1": b1m3,
            "b2": b2m3
        },
        "states": {
            "s1": s1m3,
            "s2": s2m3
        }
    }
}


sim_config = {
    "N": 2,
    "T": range(5)
}


configs.append(
    Configuration(
        sim_config=sim_config,
        state_dict=genesis_states,
        seed=seed,
        exogenous_states=exogenous_states,
        env_processes=env_processes,
        mechanisms=mechanisms
    )
)
