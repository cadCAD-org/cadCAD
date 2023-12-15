from typing import Callable, Dict, List, Any, Tuple
from pathos.multiprocessing import ProcessPool # type: ignore
from collections import Counter
from cadCAD.types import *
from cadCAD.utils import flatten

VarDictType = Dict[str, List[object]]
StatesListsType = List[dict[str, object]]
ConfigsType = List[tuple[list[callable], List[callable]]]
EnvProcessesType = Dict[str, callable]


def single_proc_exec(
    simulation_execs: List[ExecutorFunction],
    var_dict_list: List[Parameters],
    states_lists: List[StateHistory],
    configs_structs: List[StateUpdateBlocks],
    env_processes_list: List[EnvProcesses],
    Ts: List[TimeSeq],
    SimIDs: List[SimulationID],
    Ns: List[Run],
    ExpIDs: List[int],
    SubsetIDs: List[SubsetID],
    SubsetWindows: List[SubsetWindow],
    configured_n: List[N_Runs],
    additional_objs=None
):
    
    # HACK for making it run with N_Runs=1
    if type(var_dict_list) == list:
        var_dict_list = var_dict_list[0]

    print(f'Execution Mode: single_threaded')
    raw_params: List[List] = [
        simulation_execs, states_lists, configs_structs, env_processes_list,
        Ts, SimIDs, Ns, SubsetIDs, SubsetWindows
    ]
    simulation_exec, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window = list(
        map(lambda x: x.pop(), raw_params)
    )
    result = simulation_exec(
        var_dict_list, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n, additional_objs
    )
    return flatten(result)





def parallelize_simulations(
    simulation_execs: List[ExecutorFunction],
    var_dict_list: List[Parameters],
    states_lists: List[StateHistory],
    configs_structs: List[StateUpdateBlocks],
    env_processes_list: List[EnvProcesses],
    Ts: List[TimeSeq],
    SimIDs: List[SimulationID],
    Ns: List[Run],
    ExpIDs: List[int],
    SubsetIDs: List[SubsetID],
    SubsetWindows: List[SubsetWindow],
    configured_n: List[N_Runs],
    additional_objs=None
):

    print(f'Execution Mode: parallelized')
    params = list(
        zip(
            simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list,
            Ts, SimIDs, Ns, SubsetIDs, SubsetWindows
        )
    )

    len_configs_structs = len(configs_structs)

    unique_runs = Counter(SimIDs)
    sim_count = max(unique_runs.values())
    highest_divisor = int(len_configs_structs / sim_count)

    new_configs_structs, new_params = [], []
    for count in range(len(params)):
        if count == 0:
            new_params.append(
                params[count: highest_divisor]
            )
            new_configs_structs.append(
                configs_structs[count: highest_divisor]
            )
        elif count > 0:
            new_params.append(
                params[count * highest_divisor: (count + 1) * highest_divisor]
            )
            new_configs_structs.append(
                configs_structs[count * highest_divisor: (count + 1) * highest_divisor]
            )

    def process_executor(params):
        if len_configs_structs > 1:
            with ProcessPool(processes=len_configs_structs) as pp:
                results = pp.map(
                    lambda t: t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], configured_n), params
                )
        else:
            t = params[0]
            results = t[0](t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9], configured_n)
        return results

    results = flatten(list(map(lambda params: process_executor(params), new_params)))

    return results


def local_simulations(
    simulation_execs: List[ExecutorFunction],
    var_dict_list: List[Parameters],
    states_lists: List[StateHistory],
    configs_structs: List[StateUpdateBlocks],
    env_processes_list: List[EnvProcesses],
    Ts: List[TimeSeq],
    SimIDs: List[SimulationID],
    Ns: List[Run],
    ExpIDs: List[int],
    SubsetIDs: List[SubsetID],
    SubsetWindows: List[SubsetWindow],
    configured_n: List[N_Runs],
    additional_objs=None
    ):
    config_amt = len(configs_structs)

    if config_amt == 1: # and configured_n != 1
        return single_proc_exec(
            simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list,
            Ts, SimIDs, Ns, ExpIDs, SubsetIDs, SubsetWindows, configured_n, additional_objs
        )
    elif config_amt > 1: # and configured_n != 1
        return parallelize_simulations(
            simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list,
            Ts, SimIDs, Ns, ExpIDs, SubsetIDs, SubsetWindows, configured_n, additional_objs
        )
        # elif config_amt > 1 and configured_n == 1:
