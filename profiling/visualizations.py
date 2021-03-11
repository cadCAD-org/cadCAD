from tqdm.auto import tqdm
import pandas as pd
import plotly.express as px
import numpy as np


def visualize_elapsed_time_per_ts(df: pd.DataFrame) -> None:
    indexes = ['simulation', 'run', 'timestep', 'substep']

    z_df = df.set_index(indexes)
    first_time = z_df.query(
        'timestep == 1 & substep == 1').reset_index([-1, -2]).run_time
    s = (z_df.run_time - first_time)
    s.name = 'time_since_start'

    z_df = z_df.join(s)
    s = z_df.groupby(indexes[:-1]).time_since_start.max()

    fig = px.box(s.reset_index(),
                 x='timestep',
                 y='time_since_start')

    return fig


def visualize_substep_impact(df: pd.DataFrame) -> None:
    indexes = ['simulation', 'run', 'timestep', 'substep']

    new_df = df.copy()
    new_df = new_df.assign(psub_time=np.nan).set_index(indexes)

    # Calculate the run time associated with PSUBs
    for ind, gg_df in tqdm(df.query('substep > 0').groupby(indexes[:-1])):
        g_df = gg_df.reset_index()
        N_rows = len(g_df)
        substep_rows = list(range(N_rows))[1:-1:2]

        for substep_row in substep_rows:
            t1 = g_df.run_time[substep_row - 1]
            t2 = g_df.run_time[substep_row + 1]
            dt = t2 - t1
            g_df.loc[substep_row, 'psub_time'] = dt
        g_df = g_df.set_index(indexes)
        new_df.loc[g_df.index, 'psub_time'] = g_df.psub_time

    fig_df = new_df.reset_index()
    inds = fig_df.psub_time < fig_df.psub_time.quantile(0.95)
    inds &= fig_df.psub_time > fig_df.psub_time.quantile(0.05)
    fig = px.box(fig_df[inds],
                 x='substep_label',
                 y='psub_time')

    return fig
