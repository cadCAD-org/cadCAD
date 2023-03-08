from functools import reduce
from funcy import curry
from typing import Callable
from cadCAD.utils import flatten
from cadCAD.engine.utils import engine_exception

id_exception: callable = curry(engine_exception)(KeyError)(KeyError)(None)

Parameters = dict[str, object]
Substep = int
StateHistory = list[dict[str, object]]
State = dict[str, object]
PolicyInput = dict[str, object]
PolicyFunction = Callable[[Parameters,
                           Substep, StateHistory, State], PolicyInput]
Aggregator = Callable[[object, object], object]


def policy_scope_tuner(args: tuple,
                       additional_objs: object,
                       f: PolicyFunction) -> dict:
    """
    Execute cadCAD policy function.
    """
    (sweep_dict, sub_step, sL, s) = args
    if additional_objs is None:
        return f(sweep_dict, sub_step, sL, s)
    else:
        return f(sweep_dict, sub_step, sL, s, additional_objs)


def compose(init_reduction_funct: Aggregator,
            funct_list: list[Aggregator],
            val_list: dict) -> object:
    """
    Reduce the nested policy input dict into a simple one.
    """
    result, i = None, 0
    def composition(x): return [reduce(
        init_reduction_funct, x.values())] + funct_list
    for g in composition(val_list):
        if i == 0:
            result = g
            i = 1
        else:
            result = g(result)
    return result

class Executor:
    def __init__(
        self,
        policy_ops,
        policy_update_exception: callable = id_exception,
        state_update_exception: callable = id_exception
    ) -> None:

        self.policy_ops = policy_ops
        self.state_update_exception = state_update_exception
        self.policy_update_exception = policy_update_exception

    def get_policy_input(
        self,
        sweep_dict: dict[str, list[object]],
        sub_step: int,
        sL: list[dict[str, object]],
        s: dict[str, object],
        funcs: list[callable],
        additional_objs
    ) -> dict[str, object]:
        """
        Retrieves the Policy Input for usage on State Update Functions

        Arguments:
            sweep_dict - System Parameters
            sub_step - Execution order in regards to PSUBs
            sL - History of the variables state
            s - Current variables state
            funcs - list of cadCAD Policies to be executed
        """

        ops = self.policy_ops

        # Execute and retrieve policies results

        args = (sweep_dict, sub_step, sL, s)
        def execute_policy(f: PolicyFunction) -> dict:
            return policy_scope_tuner(args, additional_objs, f)

        col_results = map(execute_policy, funcs)


        # Create a nested dict containing all results combination
        # new_dict[policy_input][policy_ordinal] = policy_input_value
        new_dict: dict = {}
        for i, col_result in enumerate(col_results):
            for label, value in col_result.items():
                if label not in new_dict.keys():
                    new_dict[label] = {}
                else:
                    pass
                new_dict[label][i] = value

        # Aggregator functions
        ops_head, *ops_tail = ops

        # Function for aggregating a combination of policy inputs
        # for the same signal
        def f(val_list):
            return compose(init_reduction_funct=ops_head,
                           funct_list=ops_tail,
                           val_list=val_list)

        # Generate dict to be consumed by SUFs
        policy_input = {
            label: f(val_list)
            for label, val_list
            in new_dict.items()}

        return policy_input

    def apply_env_proc(
        self,
        sweep_dict,
        env_processes: dict[str, callable],
        state_dict: dict[str, object]
    ) -> dict[str, object]:

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

        filtered_state_dict = {
            k: v for k, v in state_dict.items() if k in env_processes.keys()}
        env_proc_dict = {
            target_field: env_composition(
                target_field, state_dict, target_value)
            for target_field, target_value in filtered_state_dict.items()
        }

        for k, v in env_proc_dict.items():
            state_dict[k] = v

        return state_dict

    # mech_step
    def partial_state_update(
        self,
        sweep_dict: dict[str, list[object]],
        sub_step: int,
        sL,
        sH,
        state_funcs: list[callable],
        policy_funcs: list[callable],
        env_processes: dict[str, callable],
        time_step: int,
        run: int,
        additional_objs
    ) -> list[dict[str, object]]:

        # last_in_obj: dict[str, object] = MappingProxyType(sL[-1])
        last_in_obj: dict[str, object] = sL[-1].copy()
        _input: dict[str, object] = self.policy_update_exception(
            self.get_policy_input(sweep_dict, sub_step, sH,
                                  last_in_obj, policy_funcs, additional_objs)
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

        last_in_copy: dict[str, object] = transfer_missing_fields(
            last_in_obj, dict(generate_record(state_funcs)))
        last_in_copy: dict[str, object] = self.apply_env_proc(
            sweep_dict, env_processes, last_in_copy)
        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run

        sL.append(last_in_copy)
        del last_in_copy

        return sL

    # mech_pipeline - state_update_block
    def state_update_pipeline(
        self,
        sweep_dict: dict[str, list[object]],
        simulation_list,
        configs: list[tuple[list[callable], list[callable]]],
        env_processes: dict[str, callable],
        time_step: int,
        run: int,
        additional_objs
    ) -> list[dict[str, object]]:

        sub_step = 0
        states_list_copy: list[dict[str, object]] = tuple(simulation_list[-1])
        genesis_states: dict[str, object] = states_list_copy[-1].copy()
#         genesis_states: dict[str, object] = states_list_copy[-1]

        if len(states_list_copy) == 1:
            genesis_states['substep'] = sub_step

        del states_list_copy
        states_list: list[dict[str, object]] = [genesis_states]

        sub_step += 1
        for [s_conf, p_conf] in configs:
            states_list: list[dict[str, object]] = self.partial_state_update(
                sweep_dict, sub_step, states_list, simulation_list, s_conf, p_conf, env_processes, time_step, run,
                additional_objs
            )
            sub_step += 1

        time_step += 1

        return states_list

    # state_update_pipeline
    def run_pipeline(
        self,
        sweep_dict: dict[str, list[object]],
        states_list: list[dict[str, object]],
        configs: list[tuple[list[callable], list[callable]]],
        env_processes: dict[str, callable],
        time_seq: range,
        run: int,
        additional_objs
    ) -> list[list[dict[str, object]]]:
        time_seq: list[int] = [x + 1 for x in time_seq]
        simulation_list: list[list[dict[str, object]]] = [states_list]

        for time_step in time_seq:
            pipe_run: list[dict[str, object]] = self.state_update_pipeline(
                sweep_dict, simulation_list, configs, env_processes, time_step, run, additional_objs
            )
            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)

        return simulation_list

    def simulation(
        self,
        sweep_dict: dict[str, list[object]],
        states_list: list[dict[str, object]],
        configs,
        env_processes: dict[str, callable],
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

        def execute_run(sweep_dict, states_list, configs, env_processes, time_seq, _run) -> list[dict[str, object]]:
            def generate_init_sys_metrics(genesis_states_list, sim_id, _subset_id, _run, _subset_window):
                for D in genesis_states_list:
                    d = D.copy()
                    d['simulation'], d['subset'], d['run'], d['substep'], d['timestep'] = \
                        sim_id, _subset_id, _run, 0, 0
                    yield d

            states_list_copy: list[dict[str, object]] = list(
                generate_init_sys_metrics(
                    tuple(states_list), simulation_id, subset_id, run, subset_window)
            )

            first_timestep_per_run: list[dict[str, object]] = self.run_pipeline(
                sweep_dict, states_list_copy, configs, env_processes, time_seq, run, additional_objs
            )
            del states_list_copy

            return first_timestep_per_run

        pipe_run = flatten(
            [execute_run(sweep_dict, states_list, configs,
                         env_processes, time_seq, run)]
        )

        return pipe_run
