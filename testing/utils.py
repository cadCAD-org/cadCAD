#
# def record_generator(row, cols):
#     return {col: row[col] for col in cols}

def gen_metric_row(row, cols):
    return ((row['run'], row['timestep'], row['substep']), {col: row[col] for col in cols})

# def gen_metric_row(row):
#     return ((row['run'], row['timestep'], row['substep']), {'s1': row['s1'], 'policies': row['policies']})

# def gen_metric_row(row):
#     return {
#         'run': row['run'],
#         'timestep': row['timestep'],
#         'substep': row['substep'],
#         's1': row['s1'],
#         'policies': row['policies']
#     }

def gen_metric_dict(df, cols):
    return dict([gen_metric_row(row, cols) for index, row in df.iterrows()])
