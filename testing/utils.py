def gen_metric_row(row):
    return ((row['run'], row['timestep'], row['substep']), {'s1': row['s1'], 'policies': row['policies']})

def gen_metric_row(row):
    return {
        'run': row['run'],
        'timestep': row['timestep'],
        'substep': row['substep'],
        's1': row['s1'],
        'policies': row['policies']
    }

def gen_metric_dict(df):
    return [gen_metric_row(row) for index, row in df.iterrows()]

def generate_assertions_df(df, expected_results, target_cols):
    def df_filter(run, timestep, substep):
        return df[
            (df['run'] == run) & (df['timestep'] == timestep) & (df['substep'] == substep)
        ][target_cols].to_dict(orient='records')[0]

    df['test'] = df.apply(
        lambda x: \
            df_filter(x['run'], x['timestep'], x['substep']) == expected_results[(x['run'], x['timestep'], x['substep'])]
        , axis=1
    )

    return df