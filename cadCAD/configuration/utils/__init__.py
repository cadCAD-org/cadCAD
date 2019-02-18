from datetime import datetime, timedelta
from decimal import Decimal
from copy import deepcopy
from fn.func import curried
import pandas as pd

from cadCAD.utils import dict_filter, contains_type


class TensorFieldReport:
    def __init__(self, config_proc):
        self.config_proc = config_proc

    def create_tensor_field(self, partial_state_updates, exo_proc, keys=['policies', 'states']):
        dfs = [self.config_proc.create_matrix_field(partial_state_updates, k) for k in keys]
        df = pd.concat(dfs, axis=1)
        for es, i in zip(exo_proc, range(len(exo_proc))):
            df['es' + str(i + 1)] = es
        df['m'] = df.index + 1
        return df


# def s_update(y, x):
#     return lambda step, sL, s, _input: (y, x)
#
#
def state_update(y, x):
    return lambda var_dict, sub_step, sL, s, _input: (y, x)


def bound_norm_random(rng, low, high):
    res = rng.normal((high+low)/2, (high-low)/6)
    if res < low or res > high:
        res = bound_norm_random(rng, low, high)
    return Decimal(res)


@curried
def proc_trigger(trigger_time, update_f, time):
    if time == trigger_time:
        return update_f
    else:
        return lambda x: x


tstep_delta = timedelta(days=0, minutes=0, seconds=30)
def time_step(dt_str, dt_format='%Y-%m-%d %H:%M:%S', _timedelta = tstep_delta):
    dt = datetime.strptime(dt_str, dt_format)
    t = dt + _timedelta
    return t.strftime(dt_format)


ep_t_delta = timedelta(days=0, minutes=0, seconds=1)
def ep_time_step(s, dt_str, fromat_str='%Y-%m-%d %H:%M:%S', _timedelta = ep_t_delta):
    if s['sub_step'] == 0:
        return time_step(dt_str, fromat_str, _timedelta)
    else:
        return dt_str

# mech_sweep_filter
def partial_state_sweep_filter(state_field, partial_state_updates):
    partial_state_dict = dict([(k, v[state_field]) for k, v in partial_state_updates.items()])
    return dict([
        (k, dict_filter(v, lambda v: isinstance(v, list))) for k, v in partial_state_dict.items()
            if contains_type(list(v.values()), list)
    ])


def state_sweep_filter(raw_exogenous_states):
    return dict([(k, v) for k, v in raw_exogenous_states.items() if isinstance(v, list)])

# sweep_mech_states
@curried
def sweep_partial_states(_type, in_config):
    configs = []
    # filtered_mech_states
    filtered_partial_states = partial_state_sweep_filter(_type, in_config.partial_state_updates)
    if len(filtered_partial_states) > 0:
        for partial_state, state_dict in filtered_partial_states.items():
            for state, state_funcs in state_dict.items():
                for f in state_funcs:
                    config = deepcopy(in_config)
                    config.partial_state_updates[partial_state][_type][state] = f
                    configs.append(config)
                    del config
    else:
        configs = [in_config]

    return configs


@curried
def sweep_states(state_type, states, in_config):
    configs = []
    filtered_states = state_sweep_filter(states)
    if len(filtered_states) > 0:
        for state, state_funcs in filtered_states.items():
            for f in state_funcs:
                config = deepcopy(in_config)
                exploded_states = deepcopy(states)
                exploded_states[state] = f
                if state_type == 'exogenous':
                    config.exogenous_states = exploded_states
                elif state_type == 'environmental':
                    config.env_processes = exploded_states
                configs.append(config)
                del config, exploded_states
    else:
        configs = [in_config]

    return configs


def exo_update_per_ts(ep):
    @curried
    def ep_decorator(f, y, var_dict, sub_step, sL, s, _input):
        if s['sub_step'] + 1 == 1:
            return f(var_dict, sub_step, sL, s, _input)
        else:
            return y, s[y]

    return {es: ep_decorator(f, es) for es, f in ep.items()}
