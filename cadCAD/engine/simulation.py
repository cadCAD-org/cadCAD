from copy import deepcopy
from fn.op import foldr, call

from cadCAD.engine.utils import engine_exception

id_exception = engine_exception(KeyError, KeyError, None)


class Executor:

    def __init__(self, policy_ops, policy_update_exception=id_exception, state_update_exception=id_exception):
        self.policy_ops = policy_ops # behavior_ops
        self.state_update_exception = state_update_exception
        self.policy_update_exception = policy_update_exception # behavior_update_exception

    # get_behavior_input
    def get_policy_input(self, var_dict, sub_step, sL, s, funcs):
        ops = self.policy_ops[::-1]

        def get_col_results(var_dict, sub_step, sL, s, funcs):
            return list(map(lambda f: f(var_dict, sub_step, sL, s), funcs))

        return foldr(call, get_col_results(var_dict, sub_step, sL, s, funcs))(ops)

    def apply_env_proc(self, env_processes, state_dict, sub_step):
        for state in state_dict.keys():
            if state in list(env_processes.keys()):
                env_state = env_processes[state]
                if (env_state.__name__ == '_curried') or (env_state.__name__ == 'proc_trigger'):
                    state_dict[state] = env_state(sub_step)(state_dict[state])
                else:
                    state_dict[state] = env_state(state_dict[state])

    # mech_step
    def partial_state_update(self, var_dict, sub_step, sL, state_funcs, policy_funcs, env_processes, time_step, run):
        last_in_obj = sL[-1]

        _input = self.policy_update_exception(self.get_policy_input(var_dict, sub_step, sL, last_in_obj, policy_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        last_in_copy = dict(
            [
                self.state_update_exception(f(var_dict, sub_step, sL, last_in_obj, _input)) for f in state_funcs
            ]
        )

        for k in last_in_obj:
            if k not in last_in_copy:
                last_in_copy[k] = last_in_obj[k]

        del last_in_obj

        self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestep'])

        last_in_copy['substep'], last_in_copy['timestep'], last_in_copy['run'] = sub_step, time_step, run
        sL.append(last_in_copy)
        del last_in_copy

        return sL


    # mech_pipeline
    def state_update_pipeline(self, var_dict, states_list, configs, env_processes, time_step, run):
        sub_step = 0
        states_list_copy = deepcopy(states_list)
        genesis_states = states_list_copy[-1]
        genesis_states['substep'], genesis_states['timestep'] = sub_step, time_step
        states_list = [genesis_states]

        sub_step += 1
        for config in configs:
            s_conf, p_conf = config[0], config[1]
            states_list = self.partial_state_update(var_dict, sub_step, states_list, s_conf, p_conf, env_processes, time_step, run)
            sub_step += 1

        time_step += 1

        return states_list

    def run_pipeline(self, var_dict, states_list, configs, env_processes, time_seq, run):
        time_seq = [x + 1 for x in time_seq]
        simulation_list = [states_list]
        for time_step in time_seq:
            pipe_run = self.state_update_pipeline(var_dict, simulation_list[-1], configs, env_processes, time_step, run)
            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)

        return simulation_list

    # ToDo: Muiltithreaded Runs
    def simulation(self, var_dict, states_list, configs, env_processes, time_seq, runs):
        pipe_run = []
        for run in range(runs):
            run += 1
            states_list_copy = deepcopy(states_list)
            head, *tail = self.run_pipeline(var_dict, states_list_copy, configs, env_processes, time_seq, run)
            genesis = head.pop()
            genesis['substep'], genesis['timestep'], genesis['run'] = 0, 0, run
            first_timestep_per_run = [genesis] + tail.pop(0)
            pipe_run += [first_timestep_per_run] + tail
            del states_list_copy

        return pipe_run
