import pandas as pd
from tabulate import tabulate

from engine.configProcessor import generate_config
from engine.mechanismExecutor import Executor
from utils.engine import flatten
from utils.ui import create_tensor_field
from engine.multiproc import parallelize_simulations

# from ui.config import state_dict, mechanisms, exogenous_states, env_processes, sim_config

import ui.config1 as conf1
import ui.config2 as conf2

def main():
    states_list1 = [conf1.state_dict]
    states_list2 = [conf2.state_dict]
    states_lists = [states_list1,states_list2]

    T = conf1.sim_config['T']
    N = conf2.sim_config['N']

    ep1 = list(conf1.exogenous_states.values())
    ep2 = list(conf2.exogenous_states.values())
    eps = [ep1, ep2]

    config1 = generate_config(conf1.state_dict, conf1.mechanisms, ep1)
    config2 = generate_config(conf2.state_dict, conf2.mechanisms, ep2)
    configs = [config1, config2]

    env_processes = [conf1.env_processes, conf2.env_processes]

    # Dimensions: N x r x mechs

    simulation1 = Executor(conf1.behavior_ops).simulation
    simulation2 = Executor(conf2.behavior_ops).simulation
    simulation_execs = [simulation1,simulation2]


    if len(configs) > 1:
        simulations = parallelize_simulations(simulation_execs, states_lists, configs, env_processes, T, N)
    # else:
    #     simulations = [simulation(states_list1, configs[0], env_processes, T, N)]

    # behavior_ops, states_list, configs, env_processes, time_seq, runs
    # result = simulation(states_list1, config1, conf1.env_processes, T, N)
    # return pd.DataFrame(flatten(result))

    mechanisms = [conf1.mechanisms, conf2.mechanisms]
    for result, mechanism, ep in list(zip(simulations, mechanisms, eps)):
        print(tabulate(create_tensor_field(mechanism, ep), headers='keys', tablefmt='psql'))
        print(tabulate(pd.DataFrame(flatten(result)), headers='keys', tablefmt='psql'))