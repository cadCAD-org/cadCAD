from pathos.threading import ThreadPool
from copy import deepcopy
from fn.op import foldr, call
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=4)

from SimCAD.utils import groupByKey, flatten, drop_right
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

    def xthreaded_env_proc(self, f, s_valx):
        if isinstance(s_valx, list):
            pool = ThreadPool(nodes=len(s_valx))  # ToDo: Optimize
            return pool.map(lambda f: f(s_valx), s_valx)
        else:
            return f(s_valx)

    def apply_env_proc(self, env_processes, state_dict, step):
        for state in state_dict.keys():
            if state in list(env_processes.keys()):
                env_state = env_processes[state]
                if (env_state.__name__ == '_curried') or (env_state.__name__ == 'proc_trigger'): # might want to change
                    state_dict[state] = self.xthreaded_env_proc(env_state(step), state_dict[state])
                else:
                    state_dict[state] = self.xthreaded_env_proc(env_state, state_dict[state])


    def xthreaded_state_update(self, fs, m_step, sL, last_in_obj, _input):
        if isinstance(fs, list):
            pool = ThreadPool(nodes=len(fs)) # ToDo: Optimize
            fx = pool.map(lambda f: f(m_step, sL, last_in_obj, _input), fs)
            return groupByKey(fx)
        else:
            return fs(m_step, sL, last_in_obj, _input)

    def mech_step(self, m_step, sL, state_funcs, behavior_funcs, env_processes, t_step, run):
        last_in_obj = sL[-1]

        _input = self.state_update_exception(self.get_behavior_input(m_step, sL, last_in_obj, behavior_funcs))

        # ToDo: add env_proc generator to `last_in_copy` iterator as wrapper function
        last_in_copy = dict([
            self.behavior_update_exception(
                self.xthreaded_state_update(f, m_step, sL, last_in_obj, _input)
            ) for f in state_funcs
        ])

        for k in last_in_obj:
            if k not in last_in_copy:
                last_in_copy[k] = last_in_obj[k]

        del last_in_obj

        # make env proc trigger field agnostic
        self.apply_env_proc(env_processes, last_in_copy, last_in_copy['timestamp']) # mutating last_in_copy


        def set_sys_metrics(m_step, t_step, run):
            last_in_copy["mech_step"], last_in_copy["time_step"], last_in_copy['run'] = m_step, t_step, run

        if any(isinstance(x, list) for x in last_in_copy.values()):
            last_in_copies = flatten(last_in_copy)
            for last_in_copy in last_in_copies:
                set_sys_metrics(m_step, t_step, run)
            sL.append(last_in_copies)
        else:
            set_sys_metrics(m_step, t_step, run)
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
        # print(genesis_states)

        m_step += 1
        for config in configs:
            s_conf, b_conf = config[0], config[1]
            last_states = states_list[-1]
            if isinstance(last_states, list):
                pool = ThreadPool(nodes=len(last_states)) # ToDo: Optimize
                dropped_right_sL = drop_right(states_list, 1)

                def multithreaded_mech_step(mod_states_list):
                    return self.mech_step(m_step, mod_states_list, s_conf, b_conf, env_processes, t_step, run)

                states_lists = pool.map(
                    lambda last_state_dict: dropped_right_sL + [last_state_dict],
                    last_states
                )
                print()
                pp.pprint(configs)
            else:
                states_lists = self.mech_step(m_step, states_list, s_conf, b_conf, env_processes, t_step, run)


            m_step += 1

        t_step += 1

        exit()

        return states_list

    # rename pipe
    def block_pipeline(self, states_list, configs, env_processes, time_seq, run):
        time_seq = [x + 1 for x in time_seq]
        simulation_list = [states_list]
        print(len(configs))
        for time_step in time_seq:
            # print(simulation_list)
            if len(simulation_list) == 1:
                pipe_run = self.mech_pipeline(simulation_list[-1], configs, env_processes, time_step, run)
            exit()
            # elif np.array(pipe_run[-1]) == 2:
            #     pipe_run = self.mech_pipeline(simulation_list[-1], configs, env_processes, time_step, run)
            # print(pipe_run)
            _, *pipe_run = pipe_run
            # print(pipe_run)
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