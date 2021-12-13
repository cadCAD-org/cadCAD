import unittest, pandas as pd
from testing.results_comparison import dataframe_difference, compare_results

expected_df = pd.read_pickle("expected_results/param_sweep_timestep1_4.pkl")
param_sweep_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
result_df = param_sweep_df[
    (param_sweep_df.index > 0) &
    (param_sweep_df['subset'] < 1) &
    (param_sweep_df['timestep'] < 2) &
    (param_sweep_df['run'] == 1)
]
result_diff = dataframe_difference(result_df, expected_df)


class timestep1psub0Test(compare_results(result_diff)):
    pass


if __name__ == '__main__':
    unittest.main()
