from functools import reduce
from fn.op import foldr
import pandas as pd

from SimCAD.utils import key_filter
from SimCAD.configuration.utils.behaviorAggregation import dict_elemwise_sum


class Configuration:
    def __init__(self, sim_config,
                 # default initial_conditions to empty dict because
                 # user may be using the state_dict argument
                 initial_conditions={},
                 seeds={},
                 exogenous_states={}, env_processes={},
                 partial_state_update_blocks={},
                 behavior_ops=[foldr(dict_elemwise_sum())],
                 **kwargs):
        self.sim_config = sim_config
        self.state_dict = initial_conditions
        self.seed = seeds
        self.exogenous_states = exogenous_states
        self.env_processes = env_processes
        self.behavior_ops = behavior_ops
        self.mechanisms = partial_state_update_blocks

        # for backwards compatibility, we accept old arguments via **kwargs
        # TODO: raise deprecation warnings
        for key, value in kwargs.items():
            if (key=='state_dict'):
                self.state_dict = value
            elif (key=='seed'):
                self.seed = value
            elif (key=='mechanisms'):
                self.mechanisms = value

        if (self.state_dict == {}):
            raise Exception('The initial conditions of the system have not been set')




class Identity:
    def __init__(self, behavior_id={'identity': 0}):
        self.beh_id_return_val = behavior_id

    def b_identity(self, step, sL, s):
        return self.beh_id_return_val

    def behavior_identity(self, k):
        return self.b_identity

    def no_state_identity(self, step, sL, s, _input):
        return None

    def state_identity(self, k):
        return lambda step, sL, s, _input: (k, s[k])

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
        if key == 'state_update_functions':
            identity = self.state_identity
        elif key == 'policies':
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

        def sanitize_mechanisms(m):
            # for backwards compatibility we accept the old keys
            # ('behaviors' and 'states') and rename them
            def rename_keys(d):
                try:
                    d['policies'] = d.pop('behaviors')
                except KeyError:
                    pass
                try:
                    d['state_update_functions'] = d.pop('states')
                except KeyError:
                    pass

            if (type(m)==list):
                for v in m:
                    rename_keys(v)
            elif (type(m)==dict):
                for k, v in mechanisms.items():
                    rename_keys(v)
            return

        if len(mechanisms) != 0:
            sanitize_mechanisms(mechanisms)
            bdf = self.create_matrix_field(mechanisms, 'policies')
            sdf = self.create_matrix_field(mechanisms, 'state_update_functions')
            sdf_values, bdf_values = no_update_handler(bdf, sdf)
            zipped_list = list(zip(sdf_values, bdf_values))
        else:
            sdf_values, bdf_values = only_ep_handler(state_dict)
            zipped_list = list(zip(sdf_values, bdf_values))

        return list(map(lambda x: (x[0] + exo_proc, x[1]), zipped_list))
