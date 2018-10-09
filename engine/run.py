from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config
from engine.configProcessor import generate_config
from engine.mechanismExecutor import simulation
from engine.utils import flatten

from tabulate import tabulate
import pandas as pd

def main():
    states_list = [state_dict]
    configs = generate_config(mechanisms, exogenous_states)
    # p = pipeline(states_list, configs, env_processes, range(10))
    N = sim_config['N']
    s = simulation(states_list, configs, env_processes, range(5), N)
    result = pd.DataFrame(flatten(s))
    print(tabulate(result, headers='keys', tablefmt='psql'))
