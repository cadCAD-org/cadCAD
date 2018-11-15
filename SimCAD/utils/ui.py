import pandas as pd
from SimCAD.utils.configProcessor import create_matrix_field

def create_tensor_field(mechanisms, exo_proc, keys=['behaviors', 'states']):
    dfs = [create_matrix_field(mechanisms, k) for k in keys]
    df = pd.concat(dfs, axis=1)
    for es, i in zip(exo_proc, range(len(exo_proc))):
        df['es'+str(i+1)] = es
    df['m'] = df.index + 1
    return df