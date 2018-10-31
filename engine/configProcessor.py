import pandas as pd
from functools import partial, reduce

def state_identity(k):
    def identity(step, sL, s, _input):
        return (k, s[k])
    return identity

def behavior_identity(k):
    def identity(step, sL, s):
        return 0
    return identity

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
    return reduce((lambda x, y: pd.concat([x, y], axis=1)), col_list)

def generate_config(mechanisms, env_poc):
    bdf = create_matrix_field(mechanisms,'behaviors')
    sdf = create_matrix_field(mechanisms,'states')
    zipped_list = list(zip(sdf.values.tolist(), bdf.values.tolist()))
    return list(map(lambda x: (x[0] + env_poc, x[1]), zipped_list))
