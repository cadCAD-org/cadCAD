import pandas as pd
from functools import reduce

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


def generate_config(state_dict, mechanisms, exo_proc):
    def no_behavior_handler(bdf, sdf):
        if bdf.empty == False:
            sdf_values, bdf_values = sdf.values.tolist(), bdf.values.tolist()
        else:
            sdf_values = sdf.values.tolist()
            bdf_values = [ [b_identity] * len(sdf_values) for n in range(mechanisms) ]
        return sdf_values, bdf_values

    def only_ep_handler(state_dict):
        sdf_functions = [ lambda step, sL, s, _input: (k, v) for k, v in zip(state_dict.keys(), state_dict.values()) ]
        sdf_values = [ sdf_functions ]
        bdf_values = [ [b_identity] * len(sdf_values) ]
        return sdf_values, bdf_values

    zipped_list = []
    if len(mechanisms) != 0:
        bdf = create_matrix_field(mechanisms, 'behaviors')
        sdf = create_matrix_field(mechanisms, 'states')
        sdf_values, bdf_values = no_behavior_handler(bdf, sdf)
        zipped_list = list(zip(sdf_values, bdf_values))
    else:
        sdf_values, bdf_values = only_ep_handler(state_dict)
        zipped_list = list(zip(sdf_values, bdf_values))

    return list(map(lambda x: (x[0] + exo_proc, x[1]), zipped_list))

def create_tensor_field(mechanisms, exo_proc, keys=['behaviors', 'states']):
    dfs = [ create_matrix_field(mechanisms, k) for k in keys ]
    df = pd.concat(dfs, axis=1)
    for es, i in zip(exo_proc, range(len(exo_proc))):
        df['es'+str(i+1)] = es
    df['m'] = df.index + 1
    return df