from decimal import Decimal
import numpy as np
from datetime import timedelta
import pprint

from SimCAD import configs
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import proc_trigger, bound_norm_random, \
    ep_time_step
from SimCAD.configuration.utils.parameterSweep import ParamSweep


pp = pprint.PrettyPrinter(indent=4)

# ToDo: handle single param sweep
beta = [Decimal(1), Decimal(2)]

seed = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}


# Behaviors per Mechanism
# @curried
def b1m1(step, sL, s):
    return {'param1': 1}
# @curried
def b2m1(step, sL, s):
    return {'param2': 4}

# @curried
def b1m2(_beta, step, sL, s):
    return {'param1': 'a', 'param2': _beta}
# @curried
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

# @curried
def s2m1(sweep_param, step, sL, s, _input):
    y = 's2'
    x = sweep_param
    return (y, x)
#
# def s2m1(step, sL, s, _input):
#     y = 's2'
#     x = 0
#     return (y, x)

# @curried
def s1m2(step, sL, s, _input):
    y = 's1'
    x = _input['param2']
    return (y, x)
# @curried
def s2m2(step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)
# @curried
def s1m3(step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)
# @curried
def s2m3(step, sL, s, _input):
    y = 's2'
    x = 0
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3

# @curried
def es3p1(param, step, sL, s, _input):
    y = 's3'
    x = s['s3'] + param
    return (y, x)
# @curried
def es4p2(param, step, sL, s, _input):
    y = 's4'
    x = s['s4'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B) + param
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
# @curried
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

# need at least 1 behaviour and 1 state function for the 1st mech with behaviors
# mechanisms = {}

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
            "b2": b2m3,
        },
        "states": {
            "s1": s1m3,
            "s2": s2m3
        }
    }
}

# ToDo: inspect ****
# ToDo: code block regenerator abstracted from user: input config module with params as convention, output it not as convention,

# ToDo: make ParamSweep a part of sim_config
sim_config = {
    "N": 2,
    "T": range(5)
    # beta
}

# beta = [1,2]
# Test
# def(beta, a, b, c):
#     return a + b + beta + beta

# ToDo: and/or, or not working
# ToDo: Abstract ParamSweep away from user
param_sweep = ParamSweep(
    sweep_list=beta,
    mechs=mechanisms,
    raw_exogenous_states=raw_exogenous_states
)

# ToDo: Make loop standard by returning single elems from ParamSweep if sweep not specified
for mechanisms, exogenous_states in zip(param_sweep.mechanisms(), param_sweep.exogenous_states()):
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
