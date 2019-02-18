from functools import reduce
from fn.op import foldr
import pandas as pd
from copy import deepcopy

from cadCAD import configs
from cadCAD.utils import key_filter
from cadCAD.configuration.utils.policyAggregation import dict_elemwise_sum
from cadCAD.configuration.utils import exo_update_per_ts


class Configuration(object):
    def __init__(self, sim_config={}, initial_state={}, seeds={}, env_processes={},
                 exogenous_states={}, partial_state_update_blocks={}, policy_ops=[foldr(dict_elemwise_sum())], **kwargs):
        self.sim_config = sim_config
        self.initial_state = initial_state
        self.seeds = seeds
        self.env_processes = env_processes
        self.exogenous_states = exogenous_states
        self.partial_state_updates = partial_state_update_blocks
        self.policy_ops = policy_ops

        # for backwards compatibility, we accept old arguments via **kwargs
        # TODO: raise specific deprecation warnings for key == 'state_dict', key == 'seed', key == 'mechanisms'
        for key, value in kwargs.items():
            if key == 'state_dict':
                self.initial_state = value
            elif key == 'seed':
                self.seeds = value
            elif key == 'mechanisms':
                self.partial_state_updates = value

        if self.initial_state == {}:
            raise Exception('The initial conditions of the system have not been set')


def append_configs(sim_configs, initial_state, seeds, raw_exogenous_states, env_processes, partial_state_update_blocks, _exo_update_per_ts=True):
    if _exo_update_per_ts is True:
        exogenous_states = exo_update_per_ts(raw_exogenous_states)
    else:
        exogenous_states = raw_exogenous_states

    if isinstance(sim_configs, list):
        for sim_config in sim_configs:
            configs.append(
                Configuration(
                    sim_config=sim_config,
                    initial_state=initial_state,
                    seeds=seeds,
                    exogenous_states=exogenous_states,
                    env_processes=env_processes,
                    partial_state_update_blocks=partial_state_update_blocks
                )
            )
    elif isinstance(sim_configs, dict):
        configs.append(
            Configuration(
                sim_config=sim_configs,
                initial_state=initial_state,
                seeds=seeds,
                exogenous_states=exogenous_states,
                env_processes=env_processes,
                partial_state_update_blocks=partial_state_update_blocks
            )
        )


class Identity:
    def __init__(self, policy_id={'identity': 0}):
        self.beh_id_return_val = policy_id

    def p_identity(self, var_dict, sub_step, sL, s):
        return self.beh_id_return_val

    def policy_identity(self, k):
        return self.p_identity

    def no_state_identity(self, var_dict, sub_step, sL, s, _input):
        return None

    def state_identity(self, k):
        return lambda var_dict, sub_step, sL, s, _input: (k, s[k])

    def apply_identity_funcs(self, identity, df, cols):
        def fillna_with_id_func(identity, df, col):
            return df[[col]].fillna(value=identity(col))

        return list(map(lambda col: fillna_with_id_func(identity, df, col), cols))


class Processor:
    def __init__(self, id=Identity()):
        self.id = id
        self.p_identity = id.p_identity
        self.policy_identity = id.policy_identity
        self.no_state_identity = id.no_state_identity
        self.state_identity = id.state_identity
        self.apply_identity_funcs = id.apply_identity_funcs

    def create_matrix_field(self, partial_state_updates, key):
        if key == 'variables':
            identity = self.state_identity
        elif key == 'policies':
            identity = self.policy_identity

        df = pd.DataFrame(key_filter(partial_state_updates, key))
        col_list = self.apply_identity_funcs(identity, df, list(df.columns))
        if len(col_list) != 0:
            return reduce((lambda x, y: pd.concat([x, y], axis=1)), col_list)
        else:
            return pd.DataFrame({'empty': []})

    def generate_config(self, initial_state, partial_state_updates, exo_proc):

        def no_update_handler(bdf, sdf):
            if (bdf.empty == False) and (sdf.empty == True):
                bdf_values = bdf.values.tolist()
                sdf_values = [[self.no_state_identity] * len(bdf_values) for m in range(len(partial_state_updates))]
                return sdf_values, bdf_values
            elif (bdf.empty == True) and (sdf.empty == False):
                sdf_values = sdf.values.tolist()
                bdf_values = [[self.p_identity] * len(sdf_values) for m in range(len(partial_state_updates))]
                return sdf_values, bdf_values
            else:
                sdf_values = sdf.values.tolist()
                bdf_values = bdf.values.tolist()
                return sdf_values, bdf_values

        def only_ep_handler(state_dict):
            sdf_functions = [
                lambda var_dict, sub_step, sL, s, _input: (k, v) for k, v in zip(state_dict.keys(), state_dict.values())
            ]
            sdf_values = [sdf_functions]
            bdf_values = [[self.p_identity] * len(sdf_values)]
            return sdf_values, bdf_values

        # backwards compatibility
        def sanitize_partial_state_updates(partial_state_updates):
            new_partial_state_updates = deepcopy(partial_state_updates)
            # for backwards compatibility we accept the old keys
            # ('behaviors' and 'states') and rename them
            def rename_keys(d):
                try:
                    d['policies'] = d.pop('behaviors')
                except KeyError:
                    pass
                try:
                    d['variables'] = d.pop('states')
                except KeyError:
                    pass

            # Also for backwards compatibility, we accept partial state update blocks both as list or dict
            # No need for a deprecation warning as it's already raised by cadCAD.utils.key_filter
            if (type(new_partial_state_updates)==list):
                for v in new_partial_state_updates:
                    rename_keys(v)
            elif (type(new_partial_state_updates)==dict):
                for k, v in new_partial_state_updates.items():
                    rename_keys(v)

            del partial_state_updates
            return new_partial_state_updates

        if len(partial_state_updates) != 0:
            partial_state_updates = sanitize_partial_state_updates(partial_state_updates)
            bdf = self.create_matrix_field(partial_state_updates, 'policies')
            sdf = self.create_matrix_field(partial_state_updates, 'variables')
            sdf_values, bdf_values = no_update_handler(bdf, sdf)
            zipped_list = list(zip(sdf_values, bdf_values))
        else:
            sdf_values, bdf_values = only_ep_handler(initial_state)
            zipped_list = list(zip(sdf_values, bdf_values))

        return list(map(lambda x: (x[0] + exo_proc, x[1]), zipped_list))
