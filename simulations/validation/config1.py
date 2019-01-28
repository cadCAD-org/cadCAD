from decimal import Decimal
import numpy as np
from datetime import timedelta
from fn.func import curried
import pprint
from copy import deepcopy
from SimCAD import configs
from SimCAD.utils import flatMap, rename
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step, param_sweep
from SimCAD.engine.utils import sweep

pp = pprint.PrettyPrinter(indent=4)

# ToDo: handle single param sweep
beta =[Decimal(1), Decimal(2)]


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

@curried
def b1m2(param, step, sL, s):
    return {'param1': 'a', 'param2': param}
#
# def b1m2(step, sL, s):
#     return {'param1': 'a', 'param2': 2}

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


# param = Decimal(11.0)
# def s2m1(step, sL, s, _input):
#     y = 's2'
#     x = _input['param2'] + param
#     return (y, x)

@curried
def s2m1(param, step, sL, s, _input):
    y = 's2'
    x = _input['param2'] + param
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
#
# def es3p1(step, sL, s, _input):
#     y = 's3'
#     x = s['s3'] * bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
#     return (y, x)

@curried
def es3p1(param, step, sL, s, _input):
    y = 's3'
    x = s['s3'] + param
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
# @curried
# def env_a(param, x):
#     return x + param
def env_a(x):
    return x
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
raw_exogenous_states = {
    "s3": es3p1, #sweep(beta, es3p1),
    "s4": es4p2,
    "timestamp": es5p2
}
exogenous_states = exo_update_per_ts(raw_exogenous_states)
exogenous_states['s3'] = rename('parameterized', es3p1)

# ToDo: make env proc trigger field agnostic
# ToDo: input json into function renaming __name__
triggered_env_b = proc_trigger('2018-10-01 15:16:25', env_b)

env_processes = {
    "s3": env_a, #sweep(beta, env_a, 'env_a'),
    "s4": rename('parameterized', triggered_env_b) #sweep(beta, triggered_env_b)
}

# ToDo: The number of values enteren in sweep should be the # of config objs created,
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
            "s2": sweep(beta, s2m1) #rename('parameterized', s2m1) #s2m1(1) #sweep(beta, s2m1)
        }
    },
    "m2": {
        "behaviors": {
            "b1": sweep(beta, b1m2), #rename('parameterized', b1m2), #b1m2(1) #sweep(beta, b1m2),
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

def mech_sweep(mechanisms):
    sweep_lists = []
    new_mechanisms = deepcopy(mechanisms)
    for mech, update_types in new_mechanisms.items():
        for update_type, fkv in update_types.items():
            for sk, vfs in fkv.items():
                id_sweep_lists = []
                if isinstance(vfs, list):
                    for vf in vfs:
                        id_sweep_lists.append({mech: {update_type: {sk: vf}}})
                if len(id_sweep_lists) != 0:
                    sweep_lists.append(id_sweep_lists)

    zipped_sweep_lists = []
    it = iter(sweep_lists)
    the_len = len(next(it))
    if all(len(l) == the_len for l in it):
        zipped_sweep_lists = list(map(lambda x: list(x), list(zip(*sweep_lists))))
    else:
        raise ValueError('not all lists have same length!')

    pp.pprint(zipped_sweep_lists)
    print()

    return list(map(lambda x: list(map(lambda y: list(y.keys()).pop(), x)), zipped_sweep_lists))


print(mech_sweep(mechanisms))
print()
pp.pprint(mechanisms)

sim_config = {
    "N": 2,
    "T": range(5)
}

# # print(rename('new', b2m2).__name__)
#
def parameterize_mechanism(mechanisms, param):
    new_mechanisms = deepcopy(mechanisms)
    for mech, update_types in new_mechanisms.items():
        for update_type, fkv in update_types.items():
            for sk, vf in fkv.items():
                if vf.__name__ == 'parameterized':
                    # print(vf.__name__)
                    new_mechanisms[mech][update_type][sk] = vf(param)

    del mechanisms
    return new_mechanisms

def parameterize_states(states_dict, param):
    new_states_dict = deepcopy(states_dict)
    for sk, vf in new_states_dict.items():
        if vf.__name__ == 'parameterized':
            print(vf.__name__)
            new_states_dict[sk] = vf(param)

    del states_dict
    return new_states_dict

# parameterize_mechanism(mechanisms, beta)
@curried
def s2m1(param, a, b, c, d):
    y = a
    x = b, + c + d + param
    return (y, x)

# print(s2m1(1)(1))
# pp.pprint(mechanisms)
# pp.pprint(parameterize_mechanism(mechanisms, 1))
# print(sweep(beta, s2m1))

# pp.pprint(parameterize_states(raw_exogenous_states, 1))
# pp.pprint(parameterize_states(env_processes, 1))


# configs.append(
#     Configuration(
#         sim_config=sim_config,
#         state_dict=genesis_states,
#         seed=seed,
#         exogenous_states=exogenous_states,
#         env_processes=env_processes,
#         mechanisms=parameterize_mechanism(mechanisms, 1)
#     )
# )

# def sweep_config(config, params):
#     new_config = deepcopy(config)
#     configs = []
#     for param in params:
#         new_config.mechanisms = parameterize_mechanism(config.mechanisms, param)
#         # new_config.raw_exogenous_states = parameterize_states(config.exogenous_states, param)
#         # new_config.env_processes = parameterize_states(config.env_processes, param)
#         configs.append(new_config)
#     del config
#     return configs


# print(sweep_config(c, beta))
#
# for config in sweep_config(c, beta):
#     configs.append(config)

# for config in param_sweep(c, raw_exogenous_states):
#     configs.append(config)



# # configs = configs +
# #
# print()
# print(len(configs))
# print()



# for g in configs:
#     print()
#     print('Configuration')
#     print()
#     pp.pprint(g.env_processes)
#     print()
#     pp.pprint(g.exogenous_states)
#     print()
#     pp.pprint(g.mechanisms)
#     print()
