import numpy as np
from datetime import timedelta

from cadCAD import configs
from cadCAD.configuration.utils import bound_norm_random, config_sim, time_step, env_trigger
from simulations.regression_tests.experiments import config1_exp

seeds = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(4)
}


# Policies per Mechanism
def p1m1(_g, step, sL, s, **kwargs):
    return {'param1': 1}
def p2m1(_g, step, sL, s, **kwargs):
    return {'param1': 1, 'param2': 4}

def p1m2(_g, step, sL, s, **kwargs):
    return {'param1': 'a', 'param2': 2}
def p2m2(_g, step, sL, s, **kwargs):
    return {'param1': 'b', 'param2': 4}

def p1m3(_g, step, sL, s, **kwargs):
    return {'param1': ['c'], 'param2': np.array([10, 100])}
def p2m3(_g, step, sL, s, **kwargs):
    return {'param1': ['d'], 'param2': np.array([20, 200])}


# Internal States per Mechanism
def s1m1(_g, step, sL, s, _input, **kwargs):
    y = 's1'
    x = s['s1'] + 1
    return (y, x)
def s2m1(_g, step, sL, s, _input, **kwargs):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m2(_g, step, sL, s, _input, **kwargs):
    y = 's1'
    x = s['s1'] + 1
    return (y, x)
def s2m2(_g, step, sL, s, _input, **kwargs):
    y = 's2'
    x = _input['param2']
    return (y, x)

def s1m3(_g, step, sL, s, _input, **kwargs):
    y = 's1'
    x = s['s1'] + 1
    return (y, x)
def s2m3(_g, step, sL, s, _input, **kwargs):
    y = 's2'
    x = _input['param2']
    return (y, x)

def policies(_g, step, sL, s, _input, **kwargs):
    y = 'policies'
    x = _input
    return (y, x)


# Exogenous States
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3

def es3(_g, step, sL, s, _input, **kwargs):
    y = 's3'
    x = s['s3'] * bound_norm_random(seeds['a'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

def es4(_g, step, sL, s, _input, **kwargs):
    y = 's4'
    x = s['s4'] * bound_norm_random(seeds['b'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

def update_timestamp(_g, step, sL, s, _input, **kwargs):
    y = 'timestamp'
    return y, time_step(dt_str=s[y], dt_format='%Y-%m-%d %H:%M:%S', _timedelta=timedelta(days=0, minutes=0, seconds=1))


# Genesis States
genesis_states = {
    's1': 0.0,
    's2': 0.0,
    's3': 1.0,
    's4': 1.0,
    'timestamp': '2018-10-01 15:16:24'
}


# Environment Process
trigger_timestamps = ['2018-10-01 15:16:25', '2018-10-01 15:16:27', '2018-10-01 15:16:29']
env_processes = {
    "s3": [lambda _g, x: 5],
    "s4": env_trigger(3)(trigger_field='timestamp', trigger_vals=trigger_timestamps, funct_list=[lambda _g, x: 10])
}


partial_state_update_block = [
    {
        "policies": {
            "b1": p1m1,
            "b2": p2m1
        },
        "variables": {
            "s1": s1m1,
            "s2": s2m1,
            "s3": es3,
            "s4": es4,
            "timestamp": update_timestamp
        }
    },
    {
        "policies": {
            "b1": p1m2,
            "b2": p2m2
        },
        "variables": {
            "s1": s1m2,
            "s2": s2m2,
            # "s3": es3p1,
            # "s4": es4p2,
        }
    },
    {
        "policies": {
            "b1": p1m3,
            "b2": p2m3
        },
        "variables": {
            "s1": s1m3,
            "s2": s2m3,
            # "s3": es3p1,
            # "s4": es4p2,
        }
    }
]

sim_config_dict = {
        "N": 1,
        "T": range(5)
    }

sim_config = config_sim(sim_config_dict)
config1_exp.append_configs(
    config_list=configs,
    user_id='user_a',
    sim_configs=sim_config,
    initial_state=genesis_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_block,
    policy_ops=[lambda a, b: a + b]
)
