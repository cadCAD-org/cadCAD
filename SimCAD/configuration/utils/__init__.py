from datetime import datetime, timedelta
from decimal import Decimal
from copy import deepcopy
from fn.func import curried
import pandas as pd
from pathos.threading import ThreadPool

from SimCAD.utils import groupByKey, dict_filter, contains_type
from SimCAD.utils import flatMap

class TensorFieldReport:
    def __init__(self, config_proc):
        self.config_proc = config_proc

    # ??? dont for-loop to apply exo_procs, use exo_proc struct
    def create_tensor_field(self, mechanisms, exo_proc, keys=['behaviors', 'states']):
        dfs = [self.config_proc.create_matrix_field(mechanisms, k) for k in keys]
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
    return lambda step, sL, s, _input: (y, x)


def bound_norm_random(rng, low, high):
    # Add RNG Seed
    res = rng.normal((high+low)/2,(high-low)/6)
    if (res<low or res>high):
        res = bound_norm_random(rng, low, high)
    return Decimal(res)


@curried
def proc_trigger(trigger_step, update_f, step):
    if step == trigger_step:
        return update_f
    else:
        return lambda x: x


# accept timedelta instead of timedelta params
t_delta = timedelta(days=0, minutes=0, seconds=30)
def time_step(dt_str, dt_format='%Y-%m-%d %H:%M:%S', _timedelta = t_delta):
    dt = datetime.strptime(dt_str, dt_format)
    t = dt + _timedelta
    return t.strftime(dt_format)


# accept timedelta instead of timedelta params
t_delta = timedelta(days=0, minutes=0, seconds=1)
def ep_time_step(s, dt_str, fromat_str='%Y-%m-%d %H:%M:%S', _timedelta = t_delta):
    if s['mech_step'] == 0:
        return time_step(dt_str, fromat_str, _timedelta)
    else:
        return dt_str


def exo_update_per_ts(ep):
    @curried
    def ep_decorator(fs, y, step, sL, s, _input):
        # print(s)
        if s['mech_step'] + 1 == 1:  # inside f body to reduce performance costs
            if isinstance(fs, list):
                pool = ThreadPool(nodes=len(fs))
                fx = pool.map(lambda f: f(step, sL, s, _input), fs)
                return groupByKey(fx)
            else:
                return fs(step, sL, s, _input)
        else:
            return (y, s[y])
    return {es: ep_decorator(f, es) for es, f in ep.items()}


def mech_sweep_filter(mech_field, mechanisms):
    mech_dict = dict([(k, v[mech_field]) for k, v in mechanisms.items()])
    return dict([
        (k, dict_filter(v, lambda v: isinstance(v, list))) for k, v in mech_dict.items()
            if contains_type(list(v.values()), list)
    ])


def state_sweep_filter(raw_exogenous_states):
    return dict([(k, v) for k, v in raw_exogenous_states.items() if isinstance(v, list)])

@curried
def sweep_mechs(_type, in_config):
    configs = []
    filtered_mech_states = mech_sweep_filter(_type, in_config.mechanisms)
    if len(filtered_mech_states) > 0:
        for mech, state_dict in filtered_mech_states.items():
            for state, state_funcs in state_dict.items():
                for f in state_funcs:
                    config = deepcopy(in_config)
                    config.mechanisms[mech][_type][state] = f
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

def param_sweep(config, raw_exogenous_states):
    return flatMap(
        sweep_states('environmental', config.env_processes),
        flatMap(
            sweep_states('exogenous', raw_exogenous_states),
            flatMap(
                sweep_mechs('states'),
                sweep_mechs('behaviors', config)
            )
        )
    )