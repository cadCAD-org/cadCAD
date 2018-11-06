import pandas as pd
from functools import partial, reduce

def state_identity(k):
    return lambda step, sL, s, _input: (k, s[k])

def b_identity(step, sL, s):
    return 0
def behavior_identity(k):
    return b_identity

def key_filter(mechanisms, keyname):
    return [ v[keyname] for k, v in mechanisms.items() ]

def fillna_with_id_func(identity, df, col):
    return df[[col]].fillna(value=identity(col))

def apply_identity_funcs(identity, df, cols):
    return list(map(lambda col: fillna_with_id_func(identity, df, col), cols))

def create_matrix_field(mechanisms, key):
    if key == 'states':
        identity = state_identity
    else:
        identity = behavior_identity
    df = pd.DataFrame(key_filter(mechanisms, key))
    col_list = apply_identity_funcs(identity, df, list(df.columns))
    if len(col_list) != 0:
        return reduce((lambda x, y: pd.concat([x, y], axis=1)), col_list)
    else:
        return pd.DataFrame({'empty' : []})


def generate_config(mechanisms, env_poc):
    def no_behavior_handler(bdf, sdf):
        if bdf.empty == False:
            sdf_values, bdf_values = sdf.values.tolist(), bdf.values.tolist()
        else:
            sdf_values = sdf.values.tolist()
            bdf_values = [[b_identity] * len(sdf_values)]
        return sdf_values, bdf_values

    bdf = create_matrix_field(mechanisms, 'behaviors')
    sdf = create_matrix_field(mechanisms, 'states')
    sdf_values, bdf_values = no_behavior_handler(bdf, sdf)
    zipped_list = list(zip(sdf_values, bdf_values))

    return list(map(lambda x: (x[0] + env_poc, x[1]), zipped_list))