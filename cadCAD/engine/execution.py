import os
from typing import Callable, Dict, Generator, List, Any, Tuple, Sequence
from pathos.multiprocessing import ProcessPool  # type: ignore
from collections import Counter
from cadCAD.types import *
from cadCAD.utils import flatten, lazy_flatten
import tempfile
import pickle
import sys
from memory_profiler import profile
import dill

VarDictType = Dict[str, List[object]]
StatesListsType = List[dict[str, object]]
ConfigsType = List[tuple[list[callable], List[callable]]]
EnvProcessesType = Dict[str, callable]


def single_proc_exec(
    simulation_execs: Sequence[ExecutorFunction],
    var_dict_list: Union[Sequence[Parameters], Parameters],
    states_lists: Sequence[StateHistory],
    configs_structs: Sequence[StateUpdateBlocks],
    env_processes_list: Sequence[EnvProcesses],
    Ts: Sequence[TimeSeq],
    SimIDs: Sequence[SimulationID],
    Ns: Sequence[Run],
    ExpIDs: Sequence[int],
    SubsetIDs: Sequence[SubsetID],
    SubsetWindows: Sequence[SubsetWindow],
    configured_n: Sequence[N_Runs],
    additional_objs=None
) -> List:

    if not isinstance(var_dict_list, Sequence):
        var_dict_list = list([var_dict_list])

    raw_params = (
        simulation_execs, states_lists, configs_structs, env_processes_list,
        Ts, SimIDs, Ns, SubsetIDs, SubsetWindows, var_dict_list)

    results: List = []
    print(f'Execution Mode: single_threaded')
    for raw_param in zip(*raw_params):
        simulation_exec, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, var_dict = raw_param
        result = simulation_exec(
            var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n, additional_objs
        )
        results.append(flatten(result))
    return flatten(results)


def process_executor(params):
    simulation_exec, var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n = params

    result = [simulation_exec(
        var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n
    )]
    return result


def process_executor_disk(params):
    simulation_exec, var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n = params

    result = [simulation_exec(
        var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window, configured_n
    )]
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'wb') as f:  # Note 'wb' for binary writing mode
        dill.dump(result, f)
    return temp_file.name


@profile
def file_handler_inc(filenames: List[str]) -> Generator[List, None, None]:
    # combined_results = []
    for file_name in filenames:
        with open(file_name, 'rb') as f:  # Note 'rb' for binary reading mode
            result = dill.load(f)
            yield result  # Yield the loaded result for immediate processing

        f.close()
        os.remove(file_name)  # Clean up temporary file


@profile
def file_handler(filenames: List[str]) -> Generator[List, None, None]:
    combined_results = []
    for file_name in filenames:
        with open(file_name, 'rb') as f:  # Note 'rb' for binary reading mode
            result = dill.load(f)
            combined_results.append(result)
            result = None
        f.close()
        os.remove(file_name)  # Clean up temporary file
    return combined_results


@profile
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
    lazy_eval = False
    if (additional_objs):
        lazy_eval = additional_objs.get('lazy_eval', False)

    params = [
        (sim_exec, var_dict, states_list, config, env_processes,
         T, sim_id, N, subset_id, subset_window, configured_n)
        for sim_exec, var_dict, states_list, config, env_processes, T, sim_id, N, subset_id, subset_window in
        zip(simulation_execs, var_dict_list, states_lists, configs_structs,
            env_processes_list, Ts, SimIDs, Ns, SubsetIDs, SubsetWindows)
    ]

    if (lazy_eval):
        with ProcessPool(maxtasksperchild=1) as pool:
            temp_files = pool.map(process_executor_disk, params)
        generator = file_handler_inc(temp_files)
        return lazy_flatten(generator)

    with ProcessPool(maxtasksperchild=1) as pool:
        results = pool.map(process_executor, params)

    return flatten(results)


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

    if config_amt == 1:  # and configured_n != 1
        return single_proc_exec(
            simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list,
            Ts, SimIDs, Ns, ExpIDs, SubsetIDs, SubsetWindows, configured_n, additional_objs
        )
    elif config_amt > 1:  # and configured_n != 1
        return parallelize_simulations(
            simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list,
            Ts, SimIDs, Ns, ExpIDs, SubsetIDs, SubsetWindows, configured_n, additional_objs
        )
        # elif config_amt > 1 and configured_n == 1:
