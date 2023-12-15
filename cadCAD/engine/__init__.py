from time import time
from typing import Callable, Dict, List, Any, Tuple, Union
from tqdm.auto import tqdm

from cadCAD.utils import flatten
from cadCAD.utils.execution import print_exec_info
from cadCAD.configuration import Configuration, Processor
from cadCAD.configuration.utils import TensorFieldReport, configs_as_objs, configs_as_dicts
from cadCAD.engine.simulation import Executor as SimExecutor
from cadCAD.engine.execution import single_proc_exec, parallelize_simulations, local_simulations
from cadCAD.types import *

VarDictType = Dict[str, List[object]]
StatesListsType = List[dict[str, object]]
ConfigsType = List[tuple[list[callable], List[callable]]]
EnvProcessesType = Dict[str, callable]


class ExecutionMode:
    local_mode = 'local_proc'
    multi_mode = 'multi_proc'
    distributed = 'dist_proc'
    single_mode = 'single_proc'
    # Backwards compatible modes below
    single_proc = 'single_proc'
    multi_proc = 'multi_proc'


def auto_mode_switcher(config_amt: int):
    try:
        if config_amt == 1:
            return ExecutionMode.single_mode, single_proc_exec
        elif (config_amt > 1):
            return ExecutionMode.multi_mode, parallelize_simulations
    except AttributeError:
        if config_amt < 1:
            raise ValueError('N must be >= 1!')


class ExecutionContext:
    def __init__(self, context=ExecutionMode.local_mode, method=None, additional_objs=None) -> None:
        self.name = context
        self.additional_objs = additional_objs
        if context == 'local_proc':
            self.method = local_simulations
        elif context == 'single_proc':
            self.method = single_proc_exec
        elif context == 'multi_proc':
            self.method = parallelize_simulations
        elif context == 'dist_proc':
            def distroduce_proc(
                    simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, SimIDs, RunIDs,
                    ExpIDs,
                    SubsetIDs,
                    SubsetWindows,
                    configured_n,  # exec_method,
                    sc, additional_objs=additional_objs
            ):
                return method(
                    simulation_execs, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, SimIDs, RunIDs,
                    ExpIDs,
                    SubsetIDs,
                    SubsetWindows,
                    configured_n,  # exec_method,
                    sc, additional_objs
                )

            self.method = distroduce_proc


class Executor:
    def __init__(self,
                 exec_context: ExecutionContext, configs: List[Configuration], sc=None, empty_return=False
                 ) -> None:
        self.sc = sc
        self.SimExecutor = SimExecutor
        self.exec_method = exec_context.method
        self.exec_context = exec_context.name
        self.additional_objs = exec_context.additional_objs
        self.configs = configs
        self.empty_return = empty_return

    def execute(self) -> Tuple[object, object, Dict[str, object]]:
        if self.empty_return is True:
            return [], [], []

        config_proc = Processor()
        create_tensor_field = TensorFieldReport(
            config_proc).create_tensor_field

        sessions = []
        var_dict_list, states_lists = [], []
        Ts, Ns, SimIDs, RunIDs = [], [], [], []
        ExpIDs, ExpWindows, SubsetIDs, SubsetWindows = [], [], [], []
        eps, configs_structs, env_processes_list = [], [], []
        partial_state_updates, sim_executors = [], []
        config_idx = 0

        # Execution Info
        print_exec_info(self.exec_context, configs_as_objs(self.configs))

        t1 = time()
        for x in tqdm(self.configs,
                      total=len(self.configs),
                      desc="Initializing configurations"):
            sessions.append(
                {
                    'user_id': x.user_id, 'experiment_id': x.experiment_id, 'session_id': x.session_id,
                    'simulation_id': x.simulation_id, 'run_id': x.run_id,
                    'subset_id': x.subset_id, 'subset_window': x.subset_window
                }
            )
            Ts.append(x.sim_config['T'])
            Ns.append(x.sim_config['N'])

            ExpIDs.append(x.experiment_id)
            ExpWindows.append(x.exp_window)
            SimIDs.append(x.simulation_id)
            SubsetIDs.append(x.subset_id)
            RunIDs.append(x.run_id)
            SubsetWindows.append(x.subset_window)

            var_dict_list.append(x.sim_config['M'])
            states_lists.append([x.initial_state])
            eps.append(list(x.exogenous_states.values()))
            configs_structs.append(config_proc.generate_config(
                x.initial_state, x.partial_state_update_blocks, eps[config_idx]))
            env_processes_list.append(x.env_processes)
            partial_state_updates.append(x.partial_state_update_blocks)
            sim_executors.append(SimExecutor(x.policy_ops).simulation)

            config_idx += 1

        remote_threshold = 100
        config_amt = len(self.configs)

        def get_final_dist_results(simulations: List[StateHistory],
                                   psus: List[StateUpdateBlocks],
                                   eps,
                                   sessions: List[SessionDict]):
            tensor_fields = [create_tensor_field(
                psu, ep) for psu, ep in list(zip(psus, eps))]
            return simulations, tensor_fields, sessions

        def get_final_results(simulations: List[StateHistory],
                              psus: List[StateUpdateBlocks],
                              eps,
                              sessions: List[SessionDict],
                              remote_threshold: int):
            flat_timesteps, tensor_fields = [], []
            for sim_result, psu, ep in tqdm(list(zip(simulations, psus, eps)),
                                            total=len(simulations),
                                            desc='Flattening results'):
                flat_timesteps.append(flatten(sim_result))
                tensor_fields.append(create_tensor_field(psu, ep))

            flat_simulations = flatten(flat_timesteps)
            if config_amt == 1:
                return simulations, tensor_fields, sessions
            elif config_amt > 1:
                return flat_simulations, tensor_fields, sessions

        final_result = None
        original_N = len(configs_as_dicts(self.configs))
        if self.exec_context != ExecutionMode.distributed:
            # Consider Legacy Support
            if self.exec_context == ExecutionMode.local_mode:
                self.exec_context, self.exec_method = auto_mode_switcher(
                    config_amt)
            elif self.exec_context == ExecutionMode.single_mode or self.exec_context == ExecutionMode.single_proc:
                self.exec_context, self.exec_method = ExecutionMode.single_mode, single_proc_exec
            elif self.exec_context == ExecutionMode.multi_mode or self.exec_context == ExecutionMode.multi_proc:
                if config_amt == 1:
                    raise ValueError("Multi mode must have at least 2 configs")
                else:
                    self.exec_context, self.exec_method = ExecutionMode.multi_mode, parallelize_simulations
            else:
                raise ValueError("Invalid execution mode specified")


            print("Execution Method: " + self.exec_method.__name__)
            simulations_results = self.exec_method(
                sim_executors, var_dict_list, states_lists, configs_structs, env_processes_list, Ts, SimIDs, RunIDs,
                ExpIDs, SubsetIDs, SubsetWindows, original_N, self.additional_objs
            )

            final_result = get_final_results(
                simulations_results, partial_state_updates, eps, sessions, remote_threshold)
        elif self.exec_context == ExecutionMode.distributed:
            print("Execution Method: " + self.exec_method.__name__)
            simulations_results = self.exec_method(
                sim_executors, var_dict_list, states_lists, configs_structs, env_processes_list, Ts,
                SimIDs, RunIDs, ExpIDs, SubsetIDs, SubsetWindows, original_N, self.sc
            )
            final_result = get_final_dist_results(
                simulations_results, partial_state_updates, eps, sessions)

        t2 = time()
        print(f"Total execution time: {t2 - t1 :.2f}s")

        return final_result
