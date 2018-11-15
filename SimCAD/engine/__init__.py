from pathos.multiprocessing import ProcessingPool as Pool

import pandas as pd
from tabulate import tabulate

from SimCAD.utils import flatten
from SimCAD.utils.ui import create_tensor_field
from SimCAD.utils.configProcessor import generate_config

class ExecutionContext(object):

    def __init__(self):
        def parallelize_simulations(fs, states_list, configs, env_processes, Ts, Ns):
            l = list(zip(fs, states_list, configs, env_processes, Ts, Ns))
            with Pool(len(configs)) as p:
                results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5]), l)

            return results

        self.parallelize_simulations = parallelize_simulations


class Executor(object):

    def __init__(self, ExecutionContext, configs):
        from SimCAD.engine.simulation import Executor

        def execute():
            ec = ExecutionContext()
            print(configs)
            states_lists, Ts, Ns, eps, configs_struct, env_processes, mechanisms, simulation_execs = \
                [], [], [], [], [], [], [], []
            config_idx = 0
            for x in configs:
                states_lists.append([x.state_dict])
                Ts.append(x.sim_config['T'])
                Ns.append(x.sim_config['N'])
                eps.append(list(x.exogenous_states.values()))
                configs_struct.append(generate_config(x.state_dict, x.mechanisms, eps[config_idx]))
                env_processes.append(x.env_processes)
                mechanisms.append(x.mechanisms)
                simulation_execs.append(Executor(x.behavior_ops).simulation)

                config_idx += 1

            # Dimensions: N x r x mechs

            if len(configs) > 1:
                simulations = ec.parallelize_simulations(simulation_execs, states_lists, configs_struct, env_processes, Ts, Ns)

                for result, mechanism, ep in list(zip(simulations, mechanisms, eps)):
                    print(tabulate(create_tensor_field(mechanism, ep), headers='keys', tablefmt='psql'))
                    print(tabulate(pd.DataFrame(flatten(result)), headers='keys', tablefmt='psql'))
            else:
                print('single note')
                simulation, states_list, config = simulation_execs.pop(), states_lists.pop(), configs_struct.pop()
                env_process = env_processes.pop()
                # simulations = [simulation(states_list, config, env_processes, T, N)]

            # behavior_ops, states_list, configs, env_processes, time_seq, runs
            # result = simulation(states_list1, config1, conf1.env_processes, T, N)
            # return pd.DataFrame(flatten(result))

        self.ExecutionContext = ExecutionContext
        self.main = execute