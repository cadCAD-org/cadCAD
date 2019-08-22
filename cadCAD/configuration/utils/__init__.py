from datetime import datetime, timedelta
from copy import deepcopy
from functools import reduce
from fn.func import curried
from funcy import curry
import pandas as pd

from cadCAD.configuration.utils.depreciationHandler import sanitize_partial_state_updates
from cadCAD.utils import dict_filter, contains_type, flatten_tabulated_dict, tabulate_dict


class TensorFieldReport:
    def __init__(self, config_proc):
        self.config_proc = config_proc

    # ToDo: backwards compatibility
    def create_tensor_field(self, partial_state_updates, exo_proc, keys = ['policies', 'variables']):

        partial_state_updates = sanitize_partial_state_updates(partial_state_updates) # Temporary

        dfs = [self.config_proc.create_matrix_field(partial_state_updates, k) for k in keys]
        df = pd.concat(dfs, axis=1)
        for es, i in zip(exo_proc, range(len(exo_proc))):
            df['es' + str(i + 1)] = es
        df['m'] = df.index + 1
        return df


def state_update(y, x):
    return lambda var_dict, sub_step, sL, s, _input: (y, x)


def bound_norm_random(rng, low, high):
    res = rng.normal((high+low)/2, (high-low)/6)
    if res < low or res > high:
        res = bound_norm_random(rng, low, high)
    # return Decimal(res)
    return float(res)


@curried
def env_proc_trigger(timestep, f, time):
    if time == timestep:
        return f
    else:
        return lambda x: x


tstep_delta = timedelta(days=0, minutes=0, seconds=30)
def time_step(dt_str, dt_format='%Y-%m-%d %H:%M:%S', _timedelta = tstep_delta):
    # print(dt_str)
    dt = datetime.strptime(dt_str, dt_format)
    t = dt + _timedelta
    return t.strftime(dt_format)


ep_t_delta = timedelta(days=0, minutes=0, seconds=1)
def ep_time_step(s_condition, dt_str, fromat_str='%Y-%m-%d %H:%M:%S', _timedelta = ep_t_delta):
    # print(dt_str)
    if s_condition:
        return time_step(dt_str, fromat_str, _timedelta)
    else:
        return dt_str


def partial_state_sweep_filter(state_field, partial_state_updates):
    partial_state_dict = dict([(k, v[state_field]) for k, v in partial_state_updates.items()])
    return dict([
        (k, dict_filter(v, lambda v: isinstance(v, list))) for k, v in partial_state_dict.items()
            if contains_type(list(v.values()), list)
    ])


def state_sweep_filter(raw_exogenous_states):
    return dict([(k, v) for k, v in raw_exogenous_states.items() if isinstance(v, list)])


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
        if s['substep'] + 1 == 1:
            return f(var_dict, sub_step, sL, s, _input)
        else:
            return y, s[y]

    return {es: ep_decorator(f, es) for es, f in ep.items()}


def trigger_condition(s, pre_conditions, cond_opp):
    condition_bools = [s[field] in precondition_values for field, precondition_values in pre_conditions.items()]
    return reduce(cond_opp, condition_bools)


def apply_state_condition(pre_conditions, cond_opp, y, f, _g, step, sL, s, _input):
    if trigger_condition(s, pre_conditions, cond_opp):
        return f(_g, step, sL, s, _input)
    else:
        return y, s[y]


def var_trigger(y, f, pre_conditions, cond_op):
    return lambda _g, step, sL, s, _input: apply_state_condition(pre_conditions, cond_op, y, f, _g, step, sL, s, _input)


def var_substep_trigger(substeps):
    def trigger(end_substep, y, f):
        pre_conditions = {'substep': substeps}
        cond_opp = lambda a, b: a and b
        return var_trigger(y, f, pre_conditions, cond_opp)

    return lambda y, f: curry(trigger)(substeps)(y)(f)


def env_trigger(end_substep):
    def trigger(end_substep, trigger_field, trigger_vals, funct_list):
        def env_update(state_dict, sweep_dict, target_value):
            state_dict_copy = deepcopy(state_dict)
            # Use supstep to simulate current sysMetrics
            if state_dict_copy['substep'] == end_substep:
                state_dict_copy['timestep'] = state_dict_copy['timestep'] + 1

            if state_dict_copy[trigger_field] in trigger_vals:
                for g in funct_list:
                    target_value = g(sweep_dict, target_value)

            del state_dict_copy
            return target_value

        return env_update

    return lambda trigger_field, trigger_vals, funct_list: \
        curry(trigger)(end_substep)(trigger_field)(trigger_vals)(funct_list)


def config_sim(d):
    def process_variables(d):
        return flatten_tabulated_dict(tabulate_dict(d))

    if "M" in d:
        return [{"N": d["N"], "T": d["T"], "M": M} for M in process_variables(d["M"])]
    else:
        d["M"] = [{}]
        return d


def psub_list(psu_block, psu_steps):
    return [psu_block[psu] for psu in psu_steps]


def psub(policies, state_updates):
    return {
        'policies': policies,
        'states': state_updates
    }


def genereate_psubs(policy_grid, states_grid, policies, state_updates):
    PSUBS = []
    for policy_ids, state_list in zip(policy_grid, states_grid):
        filtered_policies = {k: v for (k, v) in policies.items() if k in policy_ids}
        filtered_state_updates = {k: v for (k, v) in state_updates.items() if k in state_list}
        PSUBS.append(psub(filtered_policies, filtered_state_updates))

    return PSUBS


def access_block(state_history, target_field, psu_block_offset, exculsion_list=[]):
    exculsion_list += [target_field]
    def filter_history(key_list, sH):
        filter = lambda key_list: \
            lambda d: {k: v for k, v in d.items() if k not in key_list}
        return list(map(filter(key_list), sH))

    if psu_block_offset < -1:
        if len(state_history) >= abs(psu_block_offset):
            return filter_history(exculsion_list, state_history[psu_block_offset])
        else:
            return []
    elif psu_block_offset == -1:
        return filter_history(exculsion_list, state_history[psu_block_offset])
    else:
        return []