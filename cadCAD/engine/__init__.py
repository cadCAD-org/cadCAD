from pprint import pprint
from typing import Callable, Dict, List, Any, Tuple
from pathos.multiprocessing import ProcessingPool as PPool
from pathos.multiprocessing import ThreadPool as TPool
from pandas.core.frame import DataFrame
from pyspark.context import SparkContext
from pyspark import cloudpickle
import pickle

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
    dist_proc = 'dist_proc'


def single_proc_exec(
        simulation_execs: List[Callable],
        var_dict_list: List[VarDictType],
        states_lists: List[StatesListsType],
        configs_structs: List[ConfigsType],
        env_processes_list: List[EnvProcessesType],
        Ts: List[range],
        Ns: List[int],
        userIDs,
        sessionIDs,
        simulationIDs,
        runIDs: List[int],
    ):
    params = [simulation_execs, states_lists, configs_structs, env_processes_list, Ts, Ns,
              userIDs, sessionIDs, simulationIDs, runIDs]
    simulation_exec, states_list, config, env_processes, T, N, user_id, session_id, simulation_id, run_id = \
        list(map(lambda x: x.pop(), params))
    result = simulation_exec(var_dict_list, states_list, config, env_processes, T, N,
                             user_id, session_id, simulation_id, run_id)
    return flatten(result)


def parallelize_simulations(
        simulation_execs: List[Callable],
        var_dict_list: List[VarDictType],
        states_lists: List[StatesListsType],
        configs_structs: List[ConfigsType],
        env_processes_list: List[EnvProcessesType],
        Ts: List[range],
        Ns: List[int],
        userIDs,
        sessionIDs,
        simulationIDs,
        runIDs: List[int]
    ):
    params = list(zip(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                      userIDs, sessionIDs, simulationIDs, runIDs))
    with PPool(len(configs_structs)) as p:
        results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10]), params)
    return results


def distributed_simulations(
        simulation_execs: List[Callable],
        var_dict_list: List[VarDictType],
        states_lists: List[StatesListsType],
        configs_structs: List[ConfigsType],
        env_processes_list: List[EnvProcessesType],
        Ts: List[range],
        Ns: List[int],
        userIDs,
        sessionIDs,
        simulationIDs,
        runIDs: List[int],
        sc: SparkContext = None
    ):

    func_params_zipped = list(
        zip(userIDs, sessionIDs, simulationIDs, runIDs, simulation_execs, configs_structs, env_processes_list)
    )
    func_params_kv = [((t[0], t[1], t[2], t[3]), (t[4], t[5], t[6])) for t in func_params_zipped]
    def simulate(k, v):
        (sim_exec, config, env_procs) = [f[1] for f in func_params_kv if f[0] == k][0]
        print(env_procs)
        results = sim_exec(
            v['var_dict'], v['states_lists'], config, env_procs, v['Ts'], v['Ns'],
            k[0], k[1], k[2], k[3]
        )

        return results

    val_params = list(zip(userIDs, sessionIDs, simulationIDs, runIDs, var_dict_list, states_lists, Ts, Ns))
    val_params_kv = [
        (
            (t[0], t[1], t[2], t[3]),
            {'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}
        ) for t in val_params
    ]
    results_rdd = sc.parallelize(val_params_kv).map(lambda x: simulate(*x))

    return list(results_rdd.collect())


class ExecutionContext:
    def __init__(self, context: str = ExecutionMode.multi_proc) -> None:
        self.name = context
        self.method = None

        if context == 'single_proc':
            self.method = single_proc_exec
        elif context == 'multi_proc':
            self.method = parallelize_simulations
        elif context == 'dist_proc':
            self.method = distributed_simulations


class Executor:
    def __init__(self, exec_context: ExecutionContext, configs: List[Configuration], spark_context: SparkContext = None) -> None:
        self.sc = spark_context
        self.SimExecutor = SimExecutor
        self.exec_method = exec_context.method
        self.exec_context = exec_context.name
        self.configs = configs

    def execute(self) -> Tuple[List[Dict[str, Any]], DataFrame]:
        config_proc = Processor()
        create_tensor_field = TensorFieldReport(config_proc).create_tensor_field

        print(f'Execution Mode: {self.exec_context + ": " + str(self.configs)}')
        print(f'Configurations: {self.configs}')

        userIDs, sessionIDs, simulationIDs, runIDs, \
        var_dict_list, states_lists, \
        Ts, Ns, \
        eps, configs_structs, env_processes_list, \
        partial_state_updates, simulation_execs = \
            [], [], [], [], [], [], [], [], [], [], [], [], []
        config_idx = 0

        for x in self.configs:
            userIDs.append(x.user_id)
            sessionIDs.append(x.session_id)
            simulationIDs.append(x.simulation_id)
            runIDs.append(x.run_id)

            Ts.append(x.sim_config['T'])
            Ns.append(x.sim_config['N'])

            var_dict_list.append(x.sim_config['M'])
            states_lists.append([x.initial_state])
            eps.append(list(x.exogenous_states.values()))
            configs_structs.append(config_proc.generate_config(x.initial_state, x.partial_state_updates, eps[config_idx]))
            env_processes_list.append(x.env_processes)
            partial_state_updates.append(x.partial_state_updates)
            simulation_execs.append(SimExecutor(x.policy_ops).simulation)

            config_idx += 1

        if self.exec_context == ExecutionMode.single_proc:
            tensor_field = create_tensor_field(partial_state_updates.pop(), eps.pop())
            result = self.exec_method(
                simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                userIDs, sessionIDs, simulationIDs, runIDs
            )
            final_result = result, tensor_field
        else:
            if self.exec_context == ExecutionMode.multi_proc:
                # if len(self.configs) > 1:
                simulations = self.exec_method(
                    simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                    userIDs, sessionIDs, simulationIDs, runIDs
                )

            elif self.exec_context == ExecutionMode.dist_proc:
                simulations = self.exec_method(
                    simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                    userIDs, sessionIDs, simulationIDs, runIDs, self.sc
                )

            results = []
            for result, partial_state_updates, ep in list(zip(simulations, partial_state_updates, eps)):
                results.append((flatten(result), create_tensor_field(partial_state_updates, ep)))
            final_result = results

        return final_result
