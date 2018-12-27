from decimal import Decimal
import numpy as np
from datetime import timedelta

from SimCAD import configs
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step

seed = {
}

# Behaviors
# There are no behaviors in this example

# Mechanisms
# There are no mechanisms in this example

# Parameters
alfa = 1.1e-3
beta = 0.4e-3
gama = 0.4e-3
delta = 0.1e-3

# Exogenous States
def prey_model(step, sL, s, _input):
    y = 'Prey'
    x = s['Prey'] + alfa*s['Prey'] - beta*s['Prey']*s['Predator']
    return (y, x)

def predator_model(step, sL, s, _input):
    y = 'Predator'
    x = s['Predator'] + delta*s['Prey']*s['Predator'] - gama*s['Predator']
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
def time_model(step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=t_delta)
    return (y, x)

# Genesis States
genesis_states = {
    'Prey': 10,
    'Predator': 10,
    'timestamp': '2018-01-01 00:00:00'
}

# remove `exo_update_per_ts` to update every ts
exogenous_states = exo_update_per_ts(
    {
    'Prey': prey_model,
    'Predator': predator_model,
    'timestamp': time_model
    }
)

env_processes = {
}

mechanisms = {
}

sim_config = {
    'N': 1,
    'T': range(50000)
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
