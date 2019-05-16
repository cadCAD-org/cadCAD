from typing import Any, Callable, Dict, List, Tuple

from pathos.pools import ThreadPool as TPool
from copy import deepcopy
from functools import reduce
from funcy import compose

from cadCAD.engine.utils import engine_exception
from cadCAD.utils import flatten

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

        # ops = self.policy_ops[::-1]
        ops = self.policy_ops


        def get_col_results(var_dict, sub_step, sL, s, funcs):
            return list(map(lambda f: f(var_dict, sub_step, sL, s), funcs))

        def compose(init_reduction_funct, funct_list, val_list):
            result, i = None, 0
            composition = lambda x: [reduce(init_reduction_funct, x)] + funct_list
            for g in composition(val_list):
                if i == 0:
                    result = g
                    i = 1
                else:
                    result = g(result)
            return result

        col_results = get_col_results(var_dict, sub_step, sL, s, funcs)
        key_set = list(set(list(reduce(lambda a, b: a + b, list(map(lambda x: list(x.keys()), col_results))))))
        new_dict = {k: [] for k in key_set}
        for d in col_results:
            for k in d.keys():
                new_dict[k].append(d[k])

        ops_head, *ops_tail = ops
        return {
            k: compose(
                init_reduction_funct=ops_head, # func executed on value list
                funct_list=ops_tail,
                val_list=val_list
            ) for k, val_list in new_dict.items()
        }

        # [f1] = ops
        # return {k: reduce(f1, val_list) for k, val_list in new_dict.items()}
        # return foldr(call, col_results)(ops)

    # def apply_env_proc(
    #             self,
    #             env_processes: Dict[str, Callable],
    #             state_dict: Dict[str, Any],
    #             time_step: int
    #         ) -> Dict[str, Any]:
    #     for state in state_dict.keys():
    #         if state in list(env_processes.keys()):
    #             env_state: Callable = env_processes[state]
    #             if (env_state.__name__ == '_curried') or (env_state.__name__ == 'proc_trigger'):
    #                 state_dict[state] = env_state(sub_step)(state_dict[state])
    #             else:
    #                 state_dict[state] = env_state(state_dict[state])
    #
    #     return state_dict

    def apply_env_proc(
                self,
                env_processes: Dict[str, Callable],
                state_dict: Dict[str, Any],
            ) -> Dict[str, Any]:

        def env_composition(target_field, state_dict, target_value):
            function_type = type(lambda x: x)
            env_update = env_processes[target_field]
            if isinstance(env_update, list):
                target_value = compose(*env_update[::-1])(target_value)
            elif isinstance(env_update, function_type):
                target_value = env_update(state_dict, target_value)
            else:
                target_value = env_update

            return target_value

        filtered_state_dict = {k: v for k, v in state_dict.items() if k in env_processes.keys()}
        env_proc_dict = {
            target_field: env_composition(target_field, state_dict, target_value)
            for target_field, target_value in filtered_state_dict.items()
        }

        for k, v in env_proc_dict.items():
            state_dict[k] = v

        return state_dict

    # ToDo: Redifined as a function that applies the tensor field to a set og last conditions
    # mech_step
    def partial_state_update(
                self,
                var_dict: Dict[str, List[Any]],
                sub_step: int,
                sL: Any,
                sH: Any,
                state_funcs: List[Callable],
                policy_funcs: List[Callable],
                env_processes: Dict[str, Callable],
                time_step: int,
                run: int
            ) -> List[Dict[str, Any]]:

        # def dp_psu(d):
        #     for k, v in deepcopy(d).items():
        #         yield k, deepcopy(v)
        #
        # def dp_psub(l):
        #     for d in l:
        #         yield dict(dp_psu(d))

        # last_in_obj: Dict[str, Any] = dict(dp_psu(sL[-1]))

        last_in_obj: Dict[str, Any] = deepcopy(sL[-1])
        # last_in_obj: Dict[str, Any] = sL[-1]

        # last_in_obj: Dict[str, Any] = sH[-1]
        # print(last_in_obj)
        # print(sH[-1])

        _input: Dict[str, Any] = self.policy_update_exception(self.get_policy_input(var_dict, sub_step, sH, last_in_obj, policy_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        # ToDo: Can be multithreaded ??
        def generate_record(state_funcs):
            for f in state_funcs:
                yield self.state_update_exception(f(var_dict, sub_step, sH, last_in_obj, _input))

        def transfer_missing_fields(source, destination):
            for k in source:
                if k not in destination:
                    destination[k] = source[k]
            del source # last_in_obj
            return destination

        last_in_copy: Dict[str, Any] = transfer_missing_fields(last_in_obj, dict(generate_record(state_funcs)))
        # ToDo: Remove
        # last_in_copy: Dict[str, Any] = self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestep'])
        last_in_copy: Dict[str, Any] = self.apply_env_proc(env_processes, last_in_copy)


        # ToDo: make 'substep' & 'timestep' reserve fields
        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run

        sL.append(last_in_copy)
        del last_in_copy

        # print(sL)
        # print()

        return sL

    # mech_pipeline - state_update_block
    def state_update_pipeline(
                self,
                var_dict: Dict[str, List[Any]],
                simulation_list, #states_list: List[Dict[str, Any]],
                configs: List[Tuple[List[Callable], List[Callable]]],
                env_processes: Dict[str, Callable],
                time_step: int,
                run: int
            ) -> List[Dict[str, Any]]:

        sub_step = 0
        # states_list_copy: List[Dict[str, Any]] = deepcopy(states_list)
        # states_list_copy: List[Dict[str, Any]] = states_list
        # ToDo: flatten first
        # states_list_copy: List[Dict[str, Any]] = simulation_list[-1]
        states_list_copy: List[Dict[str, Any]] = deepcopy(simulation_list[-1])

        # def dp_psu(d):
        #     for k, v in deepcopy(d).items():
        #         yield k, deepcopy(v)
        #
        # def dp_psub(l):
        #     for d in l:
        #         yield dict(dp_psu(d))

        # states_list_copy: List[Dict[str, Any]] = list(dp_psub(simulation_list[-1]))
        # print(states_list_copy)

        # ToDo: Causes Substep repeats in sL:
        genesis_states: Dict[str, Any] = states_list_copy[-1]

        if len(states_list_copy) == 1:
            genesis_states['substep'] = sub_step
        #     genesis_states['timestep'] = 0
        # else:
        #     genesis_states['timestep'] = time_step

        del states_list_copy
        states_list: List[Dict[str, Any]] = [genesis_states]

        # ToDo: Causes Substep repeats in sL, use for yield
        sub_step += 1

        for [s_conf, p_conf] in configs: # tensor field

            states_list: List[Dict[str, Any]] = self.partial_state_update(
                var_dict, sub_step, states_list, simulation_list, s_conf, p_conf, env_processes, time_step, run
            )
            # print(sub_step)
            # print(simulation_list)
            # print(flatten(simulation_list))
            sub_step += 1
            # print(sub_step)

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
        # ToDo: simulation_list should be a Tensor that is generated throughout the Executor
        simulation_list: List[List[Dict[str, Any]]] = [states_list]

        # print(simulation_list[-1])
        # print()
        # pipe_run = simulation_list[-1]
        # print(simulation_list)
        for time_step in time_seq:
            pipe_run: List[Dict[str, Any]] = self.state_update_pipeline(
                var_dict, simulation_list, configs, env_processes, time_step, run
            )

            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)
            # print(simulation_list)
            # print()

        return simulation_list

    # ToDo: Below can be recieved from a tensor field
    # configs: List[Tuple[List[Callable], List[Callable]]]
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

            def generate_init_sys_metrics(genesis_states_list):
                for d in genesis_states_list:
                    d['run'], d['substep'], d['timestep'] = run, 0, 0
                    yield d

            states_list_copy: List[Dict[str, Any]] = list(generate_init_sys_metrics(deepcopy(states_list)))

            first_timestep_per_run: List[Dict[str, Any]] = self.run_pipeline(var_dict, states_list_copy, configs, env_processes, time_seq, run)
            del states_list_copy

            return first_timestep_per_run

        pipe_run: List[List[Dict[str, Any]]] = flatten(
            TPool().map(
                lambda run: execute_run(var_dict, states_list, configs, env_processes, time_seq, run),
                list(range(runs))
            )
        )

        return pipe_run
