import pandas as pd
from tabulate import tabulate

from engine.configProcessor import generate_config, create_tensor_field
from engine.mechanismExecutor import simulation
from engine.utils import flatten
from engine.multiproc import parallelize_simulations

from decimal import Decimal

# from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config

import ui.config1 as conf1
import ui.config2 as conf2

def main():
    state_dict = {
        's1': Decimal(0.0),
        's2': Decimal(0.0),
        's3': Decimal(1.0),
        's4': Decimal(1.0),
        'timestamp': '2018-10-01 15:16:24'
    }
    sim_config = {
        "N": 2,
        "T": range(5)
    }

    T = sim_config['T']
    N = sim_config['N']
    states_list = [state_dict]

    ep1 = list(conf1.exogenous_states.values())
    ep2 = list(conf2.exogenous_states.values())
    eps = [ep1,ep2]

    config1 = generate_config(conf1.state_dict, conf1.mechanisms, ep1)
    config2 = generate_config(conf2.state_dict, conf2.mechanisms, ep2)

    mechanisms = [conf1.mechanisms, conf2.mechanisms]

    configs = [config1, config2]
    env_processes = [conf1.env_processes, conf2.env_processes]

    # Dimensions: N x r x mechs

    if len(configs) > 1:
        simulations = parallelize_simulations(simulation, states_list, configs, env_processes, T, N)
    # else:
    #     simulations = [simulation(states_list, configs[0], env_processes, T, N)]

    # simulations = [simulation(states_list, config1, conf1.env_processes, T, N)]

    for result, mechanism, ep in list(zip(simulations, mechanisms, eps)):
        print(tabulate(create_tensor_field(mechanism, ep), headers='keys', tablefmt='psql'))
        print(tabulate(pd.DataFrame(flatten(result)), headers='keys', tablefmt='psql'))