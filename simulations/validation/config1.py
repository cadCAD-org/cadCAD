from decimal import Decimal
import numpy as np
from datetime import timedelta
import pprint

from SimCAD.configuration import append_configs
from SimCAD.configuration.utils import proc_trigger, bound_norm_random, ep_time_step, exo_update_per_ts

pp = pprint.PrettyPrinter(indent=4)

seed = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}

# beta = 1

# middleware(f1,f2,f3,f4)

# Behaviors per Mechanism
def b1m1(step, sL, s):
    return {'param1': 1}

def b2m1(step, sL, s):
    return {'param2': 4}

def b1m2(_beta, step, sL, s):
    return {'param1': 'a', 'param2': _beta}

def b2m2(step, sL, s):
    return {'param1': 'b', 'param2': 0}
# @curried
def b1m3(step, sL, s):
    return {'param1': np.array([10, 100])}
# @curried
def b2m3(step, sL, s):
    return {'param1': np.array([20, 200])}

# Internal States per Mechanism
# @curried
def s1m1(step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)

def s2m1(sweep_param, step, sL, s, _input):
    y = 's2'
    x = sweep_param
    return (y, x)

def s1m2(step, sL, s, _input):
    y = 's1'
    x = _input['param2']
    return (y, x)

def s2m2(step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m3(step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)

def s2m3(step, sL, s, _input):
    y = 's2'
    x = 0
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3


def es3p1(param, step, sL, s, _input):
    y = 's3'
    x = param
    return (y, x)
# @curried
def es4p2(param, step, sL, s, _input):
    y = 's4'
    x = param
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
def es5p2(step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=t_delta)
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
    'timestamp': '2018-10-01 15:16:24'
}


# remove `exo_update_per_ts` to update every ts
raw_exogenous_states = {
    "s3": es3p1, #es3p1, #sweep(beta, es3p1),
    "s4": es4p2,
    "timestamp": es5p2
}


# ToDo: make env proc trigger field agnostic
# ToDo: input json into function renaming __name__
triggered_env_b = proc_trigger('2018-10-01 15:16:25', env_b)


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
            "b2": b2m2,
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
    "T": range(5),
    "M": [Decimal(1), Decimal(2), Decimal(3)] # dict read from dict
}

append_configs(
    sim_config=sim_config,
    genesis_states=genesis_states,
    seed=seed,
    raw_exogenous_states=raw_exogenous_states,
    env_processes=env_processes,
    mechanisms=mechanisms,
    _exo_update_per_ts=True #Default
)