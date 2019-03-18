from typing import Any, Callable, Dict, List, Tuple
from pathos.pools import ThreadPool as TPool
from copy import deepcopy
from fn.op import foldr, call

from cadCAD.engine.utils import engine_exception
from cadCAD.utils import flatten
import pprint as pp

id_exception: Callable = engine_exception(KeyError, KeyError, None)


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
                    state_dict[state] = env_state(sub_step)(state_dict[state])
                else:
                    state_dict[state] = env_state(state_dict[state])

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

        last_in_obj: Dict[str, Any] = deepcopy(sL[-1])
        # last_in_obj: Dict[str, Any] = sL[-1]

        _input: Dict[str, Any] = self.policy_update_exception(self.get_policy_input(var_dict, sub_step, sL, last_in_obj, policy_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        # ToDo: Can be multithreaded ??

        # ToDo: Create Separate past state paradigm for which users specify the use of identity / past function
        # ToDo: UDC / any class must be deepcopy before every update
        # vs an assumed update

        # last_class = deepcopy(last_in_obj['classX'])

        # incoming

        # past_attr_dict = {k: v for k, v in last_in_obj.items() if
        #                  hasattr(v, 'past_attr') and k == v.past_attr}
        # incoming_attr_dict = {k: deepcopy(v) for k, v in last_in_obj.items() if
        #             hasattr(v, 'past_attr') and k != v.past_attr}

        # udcs = {k: deepcopy(v) for k, v in last_in_obj.items() if hasattr(v, 'class_id')}
        # non_udcs = {k: deepcopy(v) for k, v in last_in_obj.items() if not hasattr(v, 'class_id')}


        # past_attr_dict = {k: v for k, v in last_in_obj.items() if 'past' in v.keys()}
        # incoming_attr_dict = {k: v for k, v in last_in_obj.items() if 'current' in v.keys()}

        # ToDo: Previous Record Cache
        # last_in_copy_staging = deepcopy(last_in_obj)

        # past_udc = deepcopy(last_in_obj['classX']['current'])

        last_in_copy: Dict[str, Any] = dict(
            [
                self.state_update_exception(f(var_dict, sub_step, sL, last_in_obj, _input)) for f in state_funcs
            ]
        )

        # a b c d e f g

        for k in last_in_obj:
            if k not in last_in_copy:
                last_in_copy[k] = last_in_obj[k]

        del last_in_obj

        self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestep'])

        # ToDo: make 'substep' & 'timestep' reserve fields
        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run

        # # ToDo: Handle conditions
        # for k_past, _ in past_attr_dict.items():
        #     for _, v_current in incoming_attr_dict.items():
        #         last_in_copy[k_past] = v_current

        # last_in_copy['pastX'] = last_class

        # last_in_copy['classX']['past'] = past_udc
        # last_in_copy['pastX_str'] = past_udc

        sL.append(last_in_copy)
        del last_in_copy

        return sL

    # mech_pipeline - state_update_block
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

        # for d1 in states_list:
        #     for d2 in states_list_copy:
        #         d2['classX'] = d1['classX']

        # print()
        # pp.pprint(states_list_copy)
        # print()

        genesis_states: Dict[str, Any] = states_list_copy[-1]
        del states_list_copy
        genesis_states['substep'], genesis_states['timestep'] = sub_step, time_step
        states_list: List[Dict[str, Any]] = [genesis_states]

        sub_step += 1
        for config in configs:
            s_conf, p_conf = config[0], config[1]
            # states_list["classX"] = deepcopy(classX)
            states_list: List[Dict[str, Any]] = self.partial_state_update(
                var_dict, sub_step, states_list, s_conf, p_conf, env_processes, time_step, run
            )

            sub_step += 1

        time_step += 1

        return states_list

    # state_update_pipeline
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

    def simulation(
            self,
            var_dict: Dict[str, List[Any]],
            states_list: List[Dict[str, Any]],
            configs: List[Tuple[List[Callable], List[Callable]]],
            env_processes: Dict[str, Callable],
            time_seq: range,
            runs: int
        ) -> List[List[Dict[str, Any]]]:

        def execute_run(var_dict, states_list, configs, env_processes, time_seq, run) -> List[Dict[str, Any]]:
            run += 1
            states_list_copy: List[Dict[str, Any]] = deepcopy(states_list)

            # for d1 in states_list:
            #     for d2 in states_list_copy:
            #         d2['classX'] = d1['classX']

            head, *tail = self.run_pipeline(var_dict, states_list_copy, configs, env_processes, time_seq, run)
            del states_list_copy

            genesis: Dict[str, Any] = head.pop()
            genesis['substep'], genesis['timestep'], genesis['run'] = 0, 0, run
            first_timestep_per_run: List[Dict[str, Any]] = [genesis] + tail.pop(0)
            return [first_timestep_per_run] + tail

        pipe_run: List[List[Dict[str, Any]]] = flatten(
            TPool().map(
                lambda run: execute_run(var_dict, states_list, configs, env_processes, time_seq, run),
                list(range(runs))
            )
        )

        return pipe_run
