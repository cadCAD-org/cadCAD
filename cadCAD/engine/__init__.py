from typing import Callable, Dict, List, Any, Tuple
from pathos.multiprocessing import ProcessingPool as PPool
from pandas.core.frame import DataFrame

from cadCAD.utils import flatten
from cadCAD.configuration import Configuration, Processor
from cadCAD.configuration.utils import TensorFieldReport
from cadCAD.engine.simulation import Executor as SimExecutor

VarDictType = Dict[str, List[Any]]
StatesListsType = List[Dict[str, Any]]
ConfigsType = List[Tuple[List[Callable], List[Callable]]]
EnvProcessesType = Dict[str, Callable]


class ExecutionMode:
    single_proc = 'single_proc'
    multi_proc = 'multi_proc'


def single_proc_exec(
        simulation_execs: List[Callable],
        var_dict_list: List[VarDictType],
        states_lists: List[StatesListsType],
        configs_structs: List[ConfigsType],
        env_processes_list: List[EnvProcessesType],
        Ts: List[range],
        Ns: List[int]
    ):
    l = [simulation_execs, states_lists, configs_structs, env_processes_list, Ts, Ns]
    simulation_exec, states_list, config, env_processes, T, N = list(map(lambda x: x.pop(), l))
    result = simulation_exec(var_dict_list, states_list, config, env_processes, T, N)
    return flatten(result)


def parallelize_simulations(
        simulation_execs: List[Callable],
        var_dict_list: List[VarDictType],
        states_lists: List[StatesListsType],
        configs_structs: List[ConfigsType],
        env_processes_list: List[EnvProcessesType],
        Ts: List[range],
        Ns: List[int]
    ):
    l = list(zip(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns))
    with PPool(len(configs_structs)) as p:
        results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6]), l)
    return results


class ExecutionContext:
    def __init__(self, context: str = ExecutionMode.multi_proc) -> None:
        self.name = context
        self.method = None

        if context == 'single_proc':
            self.method = single_proc_exec
        elif context == 'multi_proc':
            self.method = parallelize_simulations


class Executor:
    def __init__(self, exec_context: ExecutionContext, configs: List[Configuration]) -> None:
        self.SimExecutor = SimExecutor
        self.exec_method = exec_context.method
        self.exec_context = exec_context.name
        self.configs = configs

    def execute(self) -> Tuple[List[Dict[str, Any]], DataFrame]:
        config_proc = Processor()
        create_tensor_field = TensorFieldReport(config_proc).create_tensor_field


        print(r'''
                            __________   ____ 
          ________ __ _____/ ____/   |  / __ \
         / ___/ __` / __  / /   / /| | / / / /
        / /__/ /_/ / /_/ / /___/ ___ |/ /_/ / 
        \___/\__,_/\__,_/\____/_/  |_/_____/  
        by BlockScience
        ''')
        print(f'Execution Mode: {self.exec_context + ": " + str(self.configs)}')
        print(f'Configurations: {self.configs}')

        var_dict_list, states_lists, Ts, Ns, eps, configs_structs, env_processes_list, partial_state_updates, simulation_execs = \
            [], [], [], [], [], [], [], [], []
        config_idx = 0

        for x in self.configs:

            Ts.append(x.sim_config['T'])
            Ns.append(x.sim_config['N'])
            var_dict_list.append(x.sim_config['M'])
            states_lists.append([x.initial_state])
            eps.append(list(x.exogenous_states.values()))
            configs_structs.append(config_proc.generate_config(x.initial_state, x.partial_state_updates, eps[config_idx]))
            # print(env_processes_list)
            env_processes_list.append(x.env_processes)
            partial_state_updates.append(x.partial_state_updates)
            simulation_execs.append(SimExecutor(x.policy_ops).simulation)

            config_idx += 1

        final_result = None

        if self.exec_context == ExecutionMode.single_proc:
            tensor_field = create_tensor_field(partial_state_updates.pop(), eps.pop())
            result = self.exec_method(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns)
            final_result = result, tensor_field
        elif self.exec_context == ExecutionMode.multi_proc:
            # if len(self.configs) > 1:
            simulations = self.exec_method(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns)
            results = []
            for result, partial_state_updates, ep in list(zip(simulations, partial_state_updates, eps)):
                results.append((flatten(result), create_tensor_field(partial_state_updates, ep)))

            final_result = results

        return final_result
