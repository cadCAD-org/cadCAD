# import libraries
from decimal import Decimal
import numpy as np
from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import bound_norm_random, ep_time_step, config_sim

seeds = {
    # 'z': np.random.RandomState(1),
    # 'a': np.random.RandomState(2)
}

sim_config = config_sim({
    'T': range(10), #number of discrete iterations in each experiement
    'N': 1, #number of times the simulation will be run (Monte Carlo runs)
    #'M': g #parameter sweep dictionary
})


# define the time deltas for the discrete increments in the model
# ts_format = '%Y-%m-%d %H:%M:%S'
# t_delta = timedelta(days=0, minutes=1, seconds=0)
# def time_model(_g, step, sL, s, _input):
#     y = 'time'
#     x = ep_time_step(s, dt_str=s['time'], fromat_str=ts_format, _timedelta=t_delta)
#     return (y, x)

# Behaviors

# Mechanisms
def update_A(_g, step, sL, s, _input):
    y = 'box_A'
    add_to_A = 0
    if (s['box_A'] > s['box_B']):
        add_to_A = -1
    elif (s['box_A'] < s['box_B']):
        add_to_A = 1
    x = s['box_A'] + add_to_A
    return (y, x)

def update_B(_g, step, sL, s, _input):
    y = 'box_B'
    add_to_B = 0
    if (s['box_B'] > s['box_A']):
        add_to_B = -1
    elif (s['box_B'] < s['box_A']):
        add_to_B = 1
    x = s['box_B'] + add_to_B
    return (y, x)

# Initial States
genesis_states = {
    'box_A': 10, # as per the description of the example, box_A starts out with 10 marbles in it
    'box_B': 0 # as per the description of the example, box_B starts out empty
}

exogenous_states = {
    #'time': time_model
}

env_processes = {
}

#build mechanism dictionary to "wire up the circuit"
mechanisms = [
    { 
        'policies': { 
        },
        'variables': { # The following state variables will be updated simultaneously
            'box_A': update_A,
            'box_B': update_B
        }
    }
]



append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    seeds=seeds,
    raw_exogenous_states=exogenous_states,
    env_processes=env_processes,
    partial_state_update_blocks=mechanisms
)
