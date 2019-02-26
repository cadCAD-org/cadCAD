from copy import deepcopy
from fn.op import foldr, call

from cadCAD.engine.utils import engine_exception
from typing import Any, Callable, Dict, List, Tuple

id_exception: Callable = engine_exception(KeyError, KeyError, None)

import pprint as pp


class Executor:

    def __init__(
                self,
                policy_ops: List[Callable],
                policy_update_exception: Callable = id_exception,
                state_update_exception: Callable = id_exception
            ) -> None:

        # behavior_ops
        self.policy_ops = policy_ops
        self.state_update_exception = state_update_exception
        self.policy_update_exception = policy_update_exception
        # behavior_update_exception

    # get_behavior_input # sL: State Window
    def get_policy_input(
                self,
                var_dict: Dict[str, List[Any]],
                sub_step: int,
                sL: List[Dict[str, Any]],
                s: Dict[str, Any],
                funcs: List[Callable]
            ) -> Dict[str, Any]:

        ops = self.policy_ops[::-1]

        def get_col_results(var_dict, sub_step, sL, s, funcs):
            return list(map(lambda f: f(var_dict, sub_step, sL, s), funcs))

        return foldr(call, get_col_results(var_dict, sub_step, sL, s, funcs))(ops)

    def apply_env_proc(
                self,
                env_processes: Dict[str, Callable],
                state_dict: Dict[str, Any],
                sub_step: int
            ) -> None:
        for state in state_dict.keys():
            if state in list(env_processes.keys()):
                env_state: Callable = env_processes[state]
                if (env_state.__name__ == '_curried') or (env_state.__name__ == 'proc_trigger'):
                    state_dict[state]: Any = env_state(sub_step)(state_dict[state])
                else:
                    state_dict[state]: Any = env_state(state_dict[state])

    # mech_step
    def partial_state_update(
                self,
                var_dict: Dict[str, List[Any]],
                sub_step: int,
                sL: Any,
                state_funcs: List[Callable],
                policy_funcs: List[Callable],
                env_processes: Dict[str, Callable],
                time_step: int,
                run: int
            ) -> List[Dict[str, Any]]:

        last_in_obj: Dict[str, Any] = sL[-1]

        _input: Dict[str, Any] = self.policy_update_exception(self.get_policy_input(var_dict, sub_step, sL, last_in_obj, policy_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        last_in_copy: Dict[str, Any] = dict(
            [
                self.state_update_exception(f(var_dict, sub_step, sL, last_in_obj, _input)) for f in state_funcs
            ]
        )

        for k in last_in_obj:
            if k not in last_in_copy:
                last_in_copy[k]: Any = last_in_obj[k]

        del last_in_obj

        self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestep'])

        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run

        sL.append(last_in_copy)
        del last_in_copy

        return sL

    # mech_pipeline
    def state_update_pipeline(
                self,
                var_dict: Dict[str, List[Any]],
                states_list: List[Dict[str, Any]],
                configs: List[Tuple[List[Callable], List[Callable]]],
                env_processes: Dict[str, Callable],
                time_step: int,
                run: int
            ) -> List[Dict[str, Any]]:

        sub_step = 0
        states_list_copy: List[Dict[str, Any]] = deepcopy(states_list)
        genesis_states: Dict[str, Any] = states_list_copy[-1]
        genesis_states['substep'], genesis_states['timestep'] = sub_step, time_step
        states_list: List[Dict[str, Any]] = [genesis_states]

        sub_step += 1
        for config in configs:
            s_conf, p_conf = config[0], config[1]
            states_list: List[Dict[str, Any]] = self.partial_state_update(
                var_dict, sub_step, states_list, s_conf, p_conf, env_processes, time_step, run
            )

            sub_step += 1

        time_step += 1

        return states_list

    def run_pipeline(
                self,
                var_dict: Dict[str, List[Any]],
                states_list: List[Dict[str, Any]],
                configs: List[Tuple[List[Callable], List[Callable]]],
                env_processes: Dict[str, Callable],
                time_seq: range,
                run: int
            ) -> List[List[Dict[str, Any]]]:

        time_seq: List[int] = [x + 1 for x in time_seq]
        simulation_list: List[List[Dict[str, Any]]] = [states_list]
        for time_step in time_seq:
            pipe_run: List[Dict[str, Any]] = self.state_update_pipeline(
                var_dict, simulation_list[-1], configs, env_processes, time_step, run
            )
            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)

        return simulation_list

    # ToDo: Muiltithreaded Runs
    def simulation(
            self,
            var_dict: Dict[str, List[Any]],
            states_list: List[Dict[str, Any]],
            configs: List[Tuple[List[Callable], List[Callable]]],
            env_processes: Dict[str, Callable],
            time_seq: range,
            runs: int
        ) -> List[List[Dict[str, Any]]]:

        pipe_run: List[List[Dict[str, Any]]] = []
        for run in range(runs):
            run += 1
            states_list_copy: List[Dict[str, Any]] = deepcopy(states_list)
            head, *tail = self.run_pipeline(var_dict, states_list_copy, configs, env_processes, time_seq, run)
            del states_list_copy

            genesis: Dict[str, Any] = head.pop()
            genesis['substep'], genesis['timestep'], genesis['run'] = 0, 0, run
            first_timestep_per_run: List[Dict[str, Any]] = [genesis] + tail.pop(0)
            pipe_run += [first_timestep_per_run] + tail

        return pipe_run
