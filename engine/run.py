from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config
from engine.configProcessor import generate_config
from engine.mechanismExecutor import simulation
from engine.utils import flatten

#from tabulate import tabulate
import pandas as pd

def main():
    states_list = [state_dict]
    configs = generate_config(mechanisms, exogenous_states)
    # p = pipeline(states_list, configs, env_processes, range(10))
    T = range(5)
    N = sim_config['N']

    # Dimensions: N x r x mechs
    s = simulation(states_list, configs, env_processes, T, N)
    result = pd.DataFrame(flatten(s))
    print('Test')
#    print(tabulate(result, headers='keys', tablefmt='psql'))
# remove print and tabulate functions, so it returns a dataframe
    return result