# import libraries
from decimal import Decimal
import numpy as np
from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import bound_norm_random, ep_time_step, config_sim

seeds = {
}

sim_config = config_sim({
    'T': range(10), 
    'N': 1
})

# Behaviors
def robot_arm(_g, step, sL, s):
    add_to_A = 0
    if (s['box_A'] > s['box_B']):
        add_to_A = -1
    elif (s['box_A'] < s['box_B']):
        add_to_A = 1
    return({'add_to_A': add_to_A, 'add_to_B': -add_to_A})


# Mechanisms
def increment_A(_g, step, sL, s, _input):
    y = 'box_A'
    x = s['box_A'] + _input['add_to_A']
    return (y, x)

def increment_B(_g, step, sL, s, _input):
    y = 'box_B'
    x = s['box_B'] + _input['add_to_B']
    return (y, x)

# Initial States
genesis_states = {
    'box_A': 10, 
    'box_B': 0 
}

exogenous_states = {
}


env_processes = {
}


mechanisms = [
    { 
        'policies': { 
            'robot_arm': robot_arm
        },
        'states': { 
            'box_A': increment_A,
            'box_B': increment_B
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