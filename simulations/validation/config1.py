from decimal import Decimal
import numpy as np
from datetime import timedelta
import pprint

from SimCAD import configs
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step, parameterize_mechanism, parameterize_states, sweep
from SimCAD.utils import rename

from fn.func import curried

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
def b1m1(param, step, sL, s):
    return {'param1': 1}
# @curried
def b2m1(param, step, sL, s):
    return {'param2': 4}

# @curried
def b1m2(param, step, sL, s):
    return {'param1': 'a', 'param2': param}
# @curried
def b2m2(param, step, sL, s):
    return {'param1': 'b', 'param2': 0}
# @curried
def b1m3(param, step, sL, s):
    return {'param1': np.array([10, 100])}
# @curried
def b2m3(param, step, sL, s):
    return {'param1': np.array([20, 200])}


# Internal States per Mechanism
# @curried
def s1m1(param, step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)

# @curried
def s2m1(param, step, sL, s, _input):
    y = 's2'
    x = param
    return (y, x)
# @curried
def s1m2(param, step, sL, s, _input):
    y = 's1'
    x = _input['param2']
    return (y, x)
# @curried
def s2m2(param, step, sL, s, _input):
    y = 's2'
    x = _input['param2']
    return (y, x)
# @curried
def s1m3(param, step, sL, s, _input):
    y = 's1'
    x = 0
    return (y, x)
# @curried
def s2m3(param, step, sL, s, _input):
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
def es5p2(param, step, sL, s, _input):
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
    "s3": sweep(beta, es3p1), #es3p1, #sweep(beta, es3p1),
    "s4": sweep(beta, es4p2),
    "timestamp": es5p2
}
exogenous_states_list = list(map(exo_update_per_ts, parameterize_states(raw_exogenous_states)))


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

# ToDo: The number of values enteren in sweep should be the # of config objs created,
# not dependent on the # of times the sweep is applied
# sweep exo_state func and point to exo-state in every other funtion
# param sweep on genesis states

# need at least 1 behaviour and 1 state function for the 1st mech with behaviors
# mechanisms = {}

#middleware(beta, [(m1, states, s2, s2m1), (m2, behaviors, b1, b1m2)], mechanisms)

mechanisms_test = {
    "m1": {
        "behaviors": {
            "b1": b1m1,#(0),
            "b2": b2m1#(0)
        },
        "states": {
            "s1": s1m1,#(0),
            "s2": "sweep"
        }
    },
    "m2": {
        "behaviors": {
            "b1": "sweep",
            "b2": b2m2,#(0)
        },
        "states": {
            "s1": s1m2,#(0),
            "s2": s2m2#(0)
        }
    },
    "m3": {
        "behaviors": {
            "b1": b1m3,#(0),
            "b2": b2m3,#(0)
        },
        "states": {
            "s1": s1m3,#(0),
            "s2": s2m3#(0)
        }
    }
}

from copy import deepcopy
from funcy import curry
from inspect import getfullargspec


def sweep_identifier(sweep_list, sweep_id_list, mechanisms):
    new_mechanisms = deepcopy(mechanisms)
    for x in sweep_id_list:
        current_f = new_mechanisms[x[0]][x[1]][x[2]]
        if current_f is 'sweep':
            new_mechanisms[x[0]][x[1]][x[2]] = sweep(sweep_list, x[3])

    # for mech, update_types in new_mechanisms.items():
    #     for update_type, fkv in update_types.items():
    #         for sk, current_f in fkv.items():
    #             if current_f != 'sweep' and isinstance(current_f, list) is False:
    #                 # new_mechanisms[mech][update_type][sk] = rename("unsweeped", current_f(0))
    #                 curried_f = curry(current_f)
    #
    #                 def uncurried_beh_func(a, b, c):
    #                     return curried_f(0)(a)(b)(c)
    #
    #                 def uncurried_state_func(a, b, c, d):
    #                     return curried_f(0)(a)(b)(c)(d)
    #
    #                 if update_type == 'behaviors':
    #                     new_mechanisms[mech][update_type][sk] = uncurried_beh_func
    #                 elif update_type == 'states':
    #                     new_mechanisms[mech][update_type][sk] = uncurried_state_func

    del mechanisms
    return new_mechanisms


sweep_id_list = [('m1', 'states', 's2', s2m1), ('m2', 'behaviors', 'b1', b1m2)]
# pp.pprint(sweep_identifier(beta, sweep_id_list, mechanisms_test))
# exit()

mechanisms = sweep_identifier(beta, sweep_id_list, mechanisms_test)

parameterized_mechanism = parameterize_mechanism(mechanisms)
pp.pprint(parameterized_mechanism)
# exit()

sim_config = {
    "N": 2,
    "T": range(5)
}

for mechanisms, exogenous_states in zip(parameterized_mechanism, exogenous_states_list):
    configs.append(
        Configuration(
            sim_config=sim_config,
            state_dict=genesis_states,
            seed=seed,
            exogenous_states=exogenous_states, #parameterize_states(raw_exogenous_states)[1],
            env_processes=env_processes,
            mechanisms=mechanisms #parameterize_mechanism(mechanisms)[1]
        )
    )
