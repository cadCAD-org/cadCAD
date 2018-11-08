from copy import deepcopy
from fn.op import foldr, call
from fn import _
from ui.config import behavior_ops

def getColResults(step, sL, s, funcs):
    return list(map(lambda f: f(step, sL, s), funcs))

# Data Type reduction
def getBehaviorInput(step, sL, s, funcs, ops = behavior_ops[::-1]):
    return foldr(call, getColResults(step, sL, s, funcs))(ops)

def apply_env_proc(env_processes, state_dict, step):
    for state in state_dict.keys():
        if state in list(env_processes.keys()):
            state_dict[state] = env_processes[state](step)(state_dict[state])

def exception_handler(f, m_step, sL, last_mut_obj, _input):
    try:
        return f(m_step, sL, last_mut_obj, _input)
    except KeyError:
        print("Exception")
        return f(m_step, sL, sL[-2], _input)


def mech_step(m_step, sL, state_funcs, behavior_funcs, env_processes, t_step):
    last_in_obj = sL[-1]

    _input = exception_handler(getBehaviorInput, m_step, sL, last_in_obj, behavior_funcs)

    last_in_copy = dict([ exception_handler(f, m_step, sL, last_in_obj, _input) for f in state_funcs ])
    del last_in_obj # print(str(m_step) + ': ' + str(last_in_copy))

    apply_env_proc(env_processes, last_in_copy, last_in_copy['timestamp']) # mutating last_in_copy

    last_in_copy["mech_step"], last_in_copy["time_step"] = m_step, t_step
    sL.append(last_in_copy)
    del last_in_copy

    return sL


def block_gen(states_list, configs, env_processes, t_step):
    m_step = 0
    states_list_copy = deepcopy(states_list)
    genesis_states = states_list_copy[-1]
    genesis_states['mech_step'], genesis_states['time_step'] = m_step, t_step
    states_list = [genesis_states]

    m_step += 1
    for config in configs:
        s_conf, b_conf = config[0], config[1]
        states_list = mech_step(m_step, states_list, s_conf, b_conf, env_processes, t_step)
        # print(b_conf)
        m_step += 1

    t_step += 1

    return states_list


# rename pipe
def pipeline(states_list, configs, env_processes, time_seq):
    time_seq = [x + 1 for x in time_seq]
    simulation_list = [states_list]
    for time_step in time_seq:
        pipeline_run = block_gen(simulation_list[-1], configs, env_processes, time_step)
        _, *pipeline_run = pipeline_run
        simulation_list.append(pipeline_run)

    return simulation_list


# Del head
def simulation(states_list, configs, env_processes, time_seq, runs):
    pipeline_run = []
    for run in range(runs):
        if run == 0:
            head, *tail = pipeline(states_list, configs, env_processes, time_seq)
            head[-1]['mech_step'], head[-1]['time_step'] = 0, 0
            simulation_list = [head] + tail
            pipeline_run += simulation_list
        else:
            transient_states_list = [pipeline_run[-1][-1]]
            _, *tail = pipeline(transient_states_list, configs, env_processes, time_seq)
            pipeline_run += tail

    return pipeline_run