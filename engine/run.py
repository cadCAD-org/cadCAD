from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config
from engine.configProcessor import generate_config, create_tensor_field
from engine.mechanismExecutor import simulation
from engine.utils import flatten
from tabulate import tabulate
import pandas as pd

def main():
    states_list = [state_dict]
    ep = list(exogenous_states.values())
    configs = generate_config(state_dict, mechanisms, ep)
    # print(len(configs))
    print(tabulate(create_tensor_field(mechanisms, ep), headers='keys', tablefmt='psql'))
    print
    # p = pipeline(states_list, configs, env_processes, range(10))
    T = sim_config['T']
    N = sim_config['N']

    # Dimensions: N x r x mechs
    s = simulation(states_list, configs, env_processes, T, N)

    result = pd.DataFrame(flatten(s))

    return result