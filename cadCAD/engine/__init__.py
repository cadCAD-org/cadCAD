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
    # params = list(zip(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
    #                   userIDs, sessionIDs, simulationIDs, runIDs))
    # lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10])
    func_params = list(
        zip(userIDs, sessionIDs, simulationIDs, runIDs, simulation_execs, configs_structs, env_processes_list)
    )

    func_params_dict = dict(
        [((t[0], t[1], t[2], t[3]), {'sim_exec': t[4], 'config': t[5], 'env_procs': t[6]}) for t in func_params]
    )

    pprint(func_params_dict)

    val_params = list(zip(userIDs, sessionIDs, simulationIDs, runIDs, var_dict_list, states_lists, Ts, Ns))
    val_params_list = [
        (
            {'user_id': t[0], 'session_id': t[1], 'sim_id': t[2], 'run_id': t[3]},
            {'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}
        ) for t in val_params
    ]

    # pprint(val_params_dict)
    def simulate(k, v):
        (sim_exec, config, env_procs) = func_params_dict(k)
        results = sim_exec(
            v['var_dict'], v['states_lists'], config, env_procs, v['Ts'], v['Ns'],
            k['user_id'], k['session_id'], k['sim_id'], k['run_id']
        )

        return results


    vals_rdd = sc.parallelize(val_params_list).map(lambda x: simulate(x[0], x[1])) #.map(lambda x: tuple(x[0].values()))
    pprint(vals_rdd.take(1))
    # vals_rdd.foreach(print)
    #     .map(
    #     lambda t: {(t[0], t[1], t[2], t[3]): {'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}}
    # )

    # params = list(zip(simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
    #                   userIDs, sessionIDs, simulationIDs, runIDs))
    # simulation_execs, configs_structs, env_processes_list

    # val_params = list(zip(userIDs, sessionIDs, simulationIDs, runIDs, var_dict_list, states_lists, Ts, Ns))
    # vals_rdd = sc.parallelize(val_params).map(
    #     lambda t: {'user_id': t[0], 'session_id': t[1], 'simulation_id': t[2], 'run_id': t[3],
    #                'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}
    # )
    # vals_rdd.foreach(print)

    # func_params_dicts = dict(map(
    #     lambda t: {'user_id': t[0], 'session_id': t[1], 'simulation_id': t[2], 'run_id': t[3],
    #                'executions': {'sim_exec': t[4], 'configs': t[5], 'env_proc': t[6]}},
    #     func_params
    # ))



    # func_params_dicts = dict(list(map(
    #     lambda t: {'key': (t[0], t[1], t[2], t[3]),
    #                'executions': {'sim_exec': t[4], 'configs': t[5], 'env_proc': t[6]}},
    #     func_params
    # )))

    # func_keys = [(t[0], t[1], t[2], t[3]) for t in func_params]
    # func_values = [(t[4], t[5], t[6], t[7]) for t in func_params]


    # func_params_dicts = dict([{(t[0], t[1], t[2], t[3]): {'sim_exec': t[4], 'configs': t[5], 'env_proc': t[6]}} for t in func_params])

    # pprint(func_params_dicts)

    # val_params = list(zip(userIDs, sessionIDs, simulationIDs, runIDs, var_dict_list, states_lists, Ts, Ns))
    # vals_rdd = sc.parallelize(val_params).map(
    #     lambda t: {'key': (t[0], t[1], t[2], t[3]),
    #                'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]}
    # )


    # val_params_dicts = list(map(
    #     lambda t: {'user_id': t[0], 'session_id': t[1], 'simulation_id': t[2], 'run_id': t[3],
    #                'var_dict': t[4], 'states_lists': t[5], 'Ts': t[6], 'Ns': t[7]},
    #     val_params
    # ))
    # pprint(val_params_dicts)
    # print("Execution: simulation_execs")
    # print("Configuation: configs_structs, env_processes_list")
    # print()

    exit()

    # Pickle send to worker
    # atom = params[0]
    # # pprint(atom)
    # sim_exec = atom[0]
    # configs_struct = atom[3]
    # env_processes = atom[4]
    # pickled_sim_exec = cloudpickle.dumps(sim_exec)
    # pickled_configs = cloudpickle.dumps(configs_struct)
    # pickled_env_procs = cloudpickle.dumps(env_processes)
    #
    # def cucumber(pickled):
    #     unpickled = pickle.loads(pickled)
    #     return unpickled
    #
    # sc.parallelize([pickled_sim_exec]).map(cucumber).collect()



    # configs_structs, simulation_execs, env_processes_list
    results = [t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], sc) for t in params]

    # def pickle_magic(cucumber):
    #     cucumber[]
    #     cloudpickle.dump()
    #     cucumber = pickle.loads(pickled)



    pickled_params = cloudpickle.dump(params)
    results = sc.parallelize(pickled_params).map(
        lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10])
    ).collect()
    # with PPool(len(configs_structs)) as p:
    #     results = p.map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10], sc), params)
    return results

    # _pickle.PicklingError: Can't pickle <function <lambda> at 0x1115149e0>: attribute lookup <lambda> on
    # simulations.regression_tests.config1 failed
    # simulation_execs, env_processes_list
    # Configuration Layer: configs_structs
    # AttributeError: Can't pickle local object 'Identity.state_identity.<locals>.<lambda>'
    # pprint(configs_structs)
    # sc.parallelize([configs_structs])
    # exit()
    # result = sc.parallelize(params) \
    #             .map(lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], t[10])) \
    #             .collect()

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

        final_result = None

        if self.exec_context == ExecutionMode.single_proc:
            tensor_field = create_tensor_field(partial_state_updates.pop(), eps.pop())
            result = self.exec_method(
                simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                userIDs, sessionIDs, simulationIDs, runIDs
            )
            final_result = result, tensor_field
        elif self.exec_context == ExecutionMode.multi_proc:
            # if len(self.configs) > 1:
            simulations = self.exec_method(
                simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                userIDs, sessionIDs, simulationIDs, runIDs
            )
            results = []
            for result, partial_state_updates, ep in list(zip(simulations, partial_state_updates, eps)):
                results.append((flatten(result), create_tensor_field(partial_state_updates, ep)))
            final_result = results
        elif self.exec_context == ExecutionMode.dist_proc:
            # if len(self.configs) > 1:
            simulations = self.exec_method(
                simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, Ns,
                userIDs, sessionIDs, simulationIDs, runIDs, self.sc
            )
            results = []
            for result, partial_state_updates, ep in list(zip(simulations, partial_state_updates, eps)):
                results.append((flatten(result), create_tensor_field(partial_state_updates, ep)))
            final_result = results

        return final_result
