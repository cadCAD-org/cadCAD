import pandas as pd
from tabulate import tabulate

from engine.configProcessor import generate_config, create_tensor_field
from engine.mechanismExecutor import simulation
from engine.utils import flatten
from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config
from engine.multiproc import parallelize_simulations


def main():
    states_list = [state_dict]
    ep = list(exogenous_states.values())
    config = generate_config(state_dict, mechanisms, ep)
    T = sim_config['T']
    N = sim_config['N']
    configs = [config, config]

    # Dimensions: N x r x mechs

    if len(configs) > 1:
     simulations = parallelize_simulations(simulation, states_list, configs, env_processes, T, N)
    else:
     simulations = [simulation(states_list, configs[0], env_processes, T, N)]

    for result in simulations:
        print(tabulate(create_tensor_field(mechanisms, ep), headers='keys', tablefmt='psql'))
        print
        print(tabulate(pd.DataFrame(flatten(result)), headers='keys', tablefmt='psql'))