from functools import reduce
from fn.op import foldr
import pandas as pd

from SimCAD import configs
from SimCAD.utils import key_filter
from SimCAD.configuration.utils.behaviorAggregation import dict_elemwise_sum
from SimCAD.configuration.utils import exo_update_per_ts


class Configuration(object):
    def __init__(self, sim_config=None, state_dict=None, seed=None, env_processes=None,
                 exogenous_states=None, mechanisms=None, behavior_ops=[foldr(dict_elemwise_sum())]):
        self.sim_config = sim_config
        self.state_dict = state_dict
        self.seed = seed
        self.env_processes = env_processes
        self.exogenous_states = exogenous_states
        self.mechanisms = mechanisms
        self.behavior_ops = behavior_ops


def append_configs(sim_configs, state_dict, seed, raw_exogenous_states, env_processes, mechanisms, _exo_update_per_ts=True):
    if _exo_update_per_ts is True:
        exogenous_states = exo_update_per_ts(raw_exogenous_states)
    else:
        exogenous_states = raw_exogenous_states

    if isinstance(sim_configs, list):
        for sim_config in sim_configs:
            configs.append(
                Configuration(
                    sim_config=sim_config,
                    state_dict=state_dict,
                    seed=seed,
                    exogenous_states=exogenous_states,
                    env_processes=env_processes,
                    mechanisms=mechanisms
                )
            )
    elif isinstance(sim_configs, dict):
        configs.append(
            Configuration(
                sim_config=sim_configs,
                state_dict=state_dict,
                seed=seed,
                exogenous_states=exogenous_states,
                env_processes=env_processes,
                mechanisms=mechanisms
            )
        )


class Identity:
    def __init__(self, behavior_id={'identity': 0}):
        self.beh_id_return_val = behavior_id

    def b_identity(self, var_dict, step, sL, s):
        return self.beh_id_return_val

    def behavior_identity(self, k):
        return self.b_identity

    def no_state_identity(self, var_dict, step, sL, s, _input):
        return None

    def state_identity(self, k):
        return lambda var_dict, step, sL, s, _input: (k, s[k])

    def apply_identity_funcs(self, identity, df, cols):
        def fillna_with_id_func(identity, df, col):
            return df[[col]].fillna(value=identity(col))

        return list(map(lambda col: fillna_with_id_func(identity, df, col), cols))


class Processor:
    def __init__(self, id=Identity()):
        self.id = id
        self.b_identity = id.b_identity
        self.behavior_identity = id.behavior_identity
        self.no_state_identity = id.no_state_identity
        self.state_identity = id.state_identity
        self.apply_identity_funcs = id.apply_identity_funcs

    def create_matrix_field(self, mechanisms, key):
        if key == 'states':
            identity = self.state_identity
        elif key == 'behaviors':
            identity = self.behavior_identity
        df = pd.DataFrame(key_filter(mechanisms, key))
        col_list = self.apply_identity_funcs(identity, df, list(df.columns))
        if len(col_list) != 0:
            return reduce((lambda x, y: pd.concat([x, y], axis=1)), col_list)
        else:
            return pd.DataFrame({'empty': []})

    def generate_config(self, state_dict, mechanisms, exo_proc):

        def no_update_handler(bdf, sdf):
            if (bdf.empty == False) and (sdf.empty == True):
                bdf_values = bdf.values.tolist()
                sdf_values = [[self.no_state_identity] * len(bdf_values) for m in range(len(mechanisms))]
                return sdf_values, bdf_values
            elif (bdf.empty == True) and (sdf.empty == False):
                sdf_values = sdf.values.tolist()
                bdf_values = [[self.b_identity] * len(sdf_values) for m in range(len(mechanisms))]
                return sdf_values, bdf_values
            else:
                sdf_values = sdf.values.tolist()
                bdf_values = bdf.values.tolist()
                return sdf_values, bdf_values

        def only_ep_handler(state_dict):
            sdf_functions = [
                lambda step, sL, s, _input: (k, v) for k, v in zip(state_dict.keys(), state_dict.values())
            ]
            sdf_values = [sdf_functions]
            bdf_values = [[self.b_identity] * len(sdf_values)]
            return sdf_values, bdf_values

        if len(mechanisms) != 0:
            bdf = self.create_matrix_field(mechanisms, 'behaviors')
            sdf = self.create_matrix_field(mechanisms, 'states')
            sdf_values, bdf_values = no_update_handler(bdf, sdf)
            zipped_list = list(zip(sdf_values, bdf_values))
        else:
            sdf_values, bdf_values = only_ep_handler(state_dict)
            zipped_list = list(zip(sdf_values, bdf_values))

        return list(map(lambda x: (x[0] + exo_proc, x[1]), zipped_list))
