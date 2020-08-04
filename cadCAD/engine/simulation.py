from typing import Any, Callable, Dict, List, Tuple
from copy import deepcopy
from functools import reduce
from funcy import curry

from cadCAD.utils import flatten
from cadCAD.engine.utils import engine_exception

id_exception: Callable = curry(engine_exception)(KeyError)(KeyError)(None)


class Executor:
    def __init__(
        self,
        policy_ops,
        policy_update_exception: Callable = id_exception,
        state_update_exception: Callable = id_exception
    ) -> None:

        self.policy_ops = policy_ops
        self.state_update_exception = state_update_exception
        self.policy_update_exception = policy_update_exception

    def get_policy_input(
        self,
        sweep_dict: Dict[str, List[Any]],
        sub_step: int,
        sL: List[Dict[str, Any]],
        s: Dict[str, Any],
        funcs: List[Callable],
        additional_objs
    ) -> Dict[str, Any]:

        ops = self.policy_ops

        def get_col_results(sweep_dict, sub_step, sL, s, funcs):
            def policy_scope_tuner(additional_objs, f):
                if additional_objs is None:
                    return f(sweep_dict, sub_step, sL, s)
                else:
                    return f(sweep_dict, sub_step, sL, s, additional_objs)
            return list(map(lambda f: policy_scope_tuner(additional_objs, f), funcs))

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

        col_results = get_col_results(sweep_dict, sub_step, sL, s, funcs)
        key_set = list(set(list(reduce(lambda a, b: a + b, list(map(lambda x: list(x.keys()), col_results))))))
        new_dict = {k: [] for k in key_set}
        for d in col_results:
            for k in d.keys():
                new_dict[k].append(d[k])

        ops_head, *ops_tail = ops
        return {
            k: compose(
                init_reduction_funct=ops_head,
                funct_list=ops_tail,
                val_list=val_list
            ) for k, val_list in new_dict.items()
        }

    def apply_env_proc(
        self,
        sweep_dict,
        env_processes: Dict[str, Callable],
        state_dict: Dict[str, Any]
    ) -> Dict[str, Any]:

        def env_composition(target_field, state_dict, target_value):
            function_type = type(lambda x: x)
            env_update = env_processes[target_field]
            if isinstance(env_update, list):
                for f in env_update:
                    target_value = f(sweep_dict, target_value)
            elif isinstance(env_update, function_type):
                target_value = env_update(state_dict, sweep_dict, target_value)
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

    # mech_step
    def partial_state_update(
        self,
        sweep_dict: Dict[str, List[Any]],
        sub_step: int,
        sL,
        sH,
        state_funcs: List[Callable],
        policy_funcs: List[Callable],
        env_processes: Dict[str, Callable],
        time_step: int,
        run: int,
        additional_objs
    ) -> List[Dict[str, Any]]:

        # last_in_obj: Dict[str, Any] = MappingProxyType(sL[-1])
        last_in_obj: Dict[str, Any] = deepcopy(sL[-1])
        _input: Dict[str, Any] = self.policy_update_exception(
            self.get_policy_input(sweep_dict, sub_step, sH, last_in_obj, policy_funcs, additional_objs)
        )

        def generate_record(state_funcs):
            def state_scope_tuner(f):
                lenf = f.__code__.co_argcount
                if lenf == 5:
                    return self.state_update_exception(f(sweep_dict, sub_step, sH, last_in_obj, _input))
                elif lenf == 6:
                    return self.state_update_exception(f(sweep_dict, sub_step, sH, last_in_obj, _input, additional_objs))
            for f in state_funcs:
                yield state_scope_tuner(f)

        def transfer_missing_fields(source, destination):
            for k in source:
                if k not in destination:
                    destination[k] = source[k]
            del source
            return destination

        last_in_copy: Dict[str, Any] = transfer_missing_fields(last_in_obj, dict(generate_record(state_funcs)))
        last_in_copy: Dict[str, Any] = self.apply_env_proc(sweep_dict, env_processes, last_in_copy)
        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run

        sL.append(last_in_copy)
        del last_in_copy

        return sL

    # mech_pipeline - state_update_block
    def state_update_pipeline(
        self,
        sweep_dict: Dict[str, List[Any]],
        simulation_list,
        configs: List[Tuple[List[Callable], List[Callable]]],
        env_processes: Dict[str, Callable],
        time_step: int,
        run: int,
        additional_objs
    ) -> List[Dict[str, Any]]:

        sub_step = 0
        states_list_copy: List[Dict[str, Any]] = tuple(simulation_list[-1])
        genesis_states: Dict[str, Any] = states_list_copy[-1].copy()
#         genesis_states: Dict[str, Any] = states_list_copy[-1]

        if len(states_list_copy) == 1:
            genesis_states['substep'] = sub_step

        del states_list_copy
        states_list: List[Dict[str, Any]] = [genesis_states]

        sub_step += 1
        for [s_conf, p_conf] in configs:
            states_list: List[Dict[str, Any]] = self.partial_state_update(
                sweep_dict, sub_step, states_list, simulation_list, s_conf, p_conf, env_processes, time_step, run,
                additional_objs
            )
            sub_step += 1

        time_step += 1

        return states_list

    # state_update_pipeline
    def run_pipeline(
        self,
        sweep_dict: Dict[str, List[Any]],
        states_list: List[Dict[str, Any]],
        configs: List[Tuple[List[Callable], List[Callable]]],
        env_processes: Dict[str, Callable],
        time_seq: range,
        run: int,
        additional_objs
    ) -> List[List[Dict[str, Any]]]:
        time_seq: List[int] = [x + 1 for x in time_seq]
        simulation_list: List[List[Dict[str, Any]]] = [states_list]

        for time_step in time_seq:
            pipe_run: List[Dict[str, Any]] = self.state_update_pipeline(
                sweep_dict, simulation_list, configs, env_processes, time_step, run, additional_objs
            )

            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)

        return simulation_list

    def simulation(
        self,
        sweep_dict: Dict[str, List[Any]],
        states_list: List[Dict[str, Any]],
        configs,
        env_processes: Dict[str, Callable],
        time_seq: range,
        simulation_id: int,
        run: int,
        subset_id,
        subset_window,
        configured_N,
        # remote_ind
        additional_objs=None
    ):
        run += 1

        subset_window.appendleft(subset_id)
        latest_subset_id, previous_subset_id = tuple(subset_window)

        if configured_N == 1 and latest_subset_id > previous_subset_id:
            run -= 1

        def execute_run(sweep_dict, states_list, configs, env_processes, time_seq, _run) -> List[Dict[str, Any]]:
            def generate_init_sys_metrics(genesis_states_list, sim_id, _subset_id, _run, _subset_window):
                for D in genesis_states_list:
                    d = deepcopy(D)
                    d['simulation'], d['subset'], d['run'], d['substep'], d['timestep'] = \
                        sim_id, _subset_id, _run, 0, 0
                    yield d

            states_list_copy: List[Dict[str, Any]] = list(
                generate_init_sys_metrics(tuple(states_list), simulation_id, subset_id, run, subset_window)
            )

            first_timestep_per_run: List[Dict[str, Any]] = self.run_pipeline(
                sweep_dict, states_list_copy, configs, env_processes, time_seq, run, additional_objs
            )
            del states_list_copy

            return first_timestep_per_run

        pipe_run = flatten(
            [execute_run(sweep_dict, states_list, configs, env_processes, time_seq, run)]
        )

        return pipe_run
