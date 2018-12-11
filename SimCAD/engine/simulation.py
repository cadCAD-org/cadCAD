from copy import deepcopy
from fn.op import foldr, call

from SimCAD.utils import rename
from SimCAD.engine.utils import engine_exception


id_exception = engine_exception(KeyError, KeyError, None)


class Executor:
    def __init__(self, behavior_ops, behavior_update_exception=id_exception, state_update_exception=id_exception):
        self.behavior_ops = behavior_ops
        self.state_update_exception = state_update_exception
        self.behavior_update_exception = behavior_update_exception

    # Data Type reduction
    def get_behavior_input(self, step, sL, s, funcs):
        ops = self.behavior_ops[::-1]

        def get_col_results(step, sL, s, funcs):
            return list(map(lambda f: f(step, sL, s), funcs))

        return foldr(call, get_col_results(step, sL, s, funcs))(ops)

    def apply_env_proc(self, env_processes, state_dict, step):
        for state in state_dict.keys():
            if state in list(env_processes.keys()):
                env_state = env_processes[state]
                if (env_state.__name__ == '_curried') or (env_state.__name__ == 'proc_trigger'): # might want to change
                    state_dict[state] = env_state(step)(state_dict[state])
                else:
                    state_dict[state] = env_state(state_dict[state])


    def mech_step(self, m_step, sL, state_funcs, behavior_funcs, env_processes, t_step, run):
        last_in_obj = sL[-1]

        _input = self.state_update_exception(self.get_behavior_input(m_step, sL, last_in_obj, behavior_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        last_in_copy = dict([self.behavior_update_exception(f(m_step, sL, last_in_obj, _input)) for f in state_funcs])

        for k in last_in_obj:
            if k not in last_in_copy:
                last_in_copy[k] = last_in_obj[k]

        del last_in_obj

        # make env proc trigger field agnostic
        self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestamp']) # mutating last_in_copy

        last_in_copy["mech_step"], last_in_copy["time_step"], last_in_copy['run'] = m_step, t_step, run
        sL.append(last_in_copy)
        del last_in_copy

        return sL

    def mech_pipeline(self, states_list, configs, env_processes, t_step, run):
        m_step = 0
        states_list_copy = deepcopy(states_list)
        # print(states_list_copy)
        # remove copy
        genesis_states = states_list_copy[-1]
        genesis_states['mech_step'], genesis_states['time_step'] = m_step, t_step
        states_list = [genesis_states]

        m_step += 1
        for config in configs:
            s_conf, b_conf = config[0], config[1]
            states_list = self.mech_step(m_step, states_list, s_conf, b_conf, env_processes, t_step, run)
            m_step += 1

        t_step += 1

        return states_list

    # rename pipe
    def block_pipeline(self, states_list, configs, env_processes, time_seq, run):
        time_seq = [x + 1 for x in time_seq]
        simulation_list = [states_list]
        # print(len(configs))
        for time_step in time_seq:
            pipe_run = self.mech_pipeline(simulation_list[-1], configs, env_processes, time_step, run)
            _, *pipe_run = pipe_run
            simulation_list.append(pipe_run)

        return simulation_list

    # Del _ / head
    def simulation(self, states_list, configs, env_processes, time_seq, runs):
        pipe_run = []
        for run in range(runs):
            run += 1
            states_list_copy = deepcopy(states_list) # WHY ???
            head, *tail = self.block_pipeline(states_list_copy, configs, env_processes, time_seq, run)
            genesis = head.pop()
            genesis['mech_step'], genesis['time_step'], genesis['run'] = 0, 0, run
            first_timestep_per_run = [genesis] + tail.pop(0)
            pipe_run += [first_timestep_per_run] + tail
            del states_list_copy

        return pipe_run