import pandas as pd
from testing.results_comparison import dataframe_difference, compare_results_pytest
import pytest


@pytest.fixture
def Timestep1Psub0():
    expected_df = pd.read_pickle("expected_results/param_sweep_timestep1_4.pkl")
    param_sweep_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
    result_df = param_sweep_df[
        (param_sweep_df.index > 0) &
        (param_sweep_df['subset'] < 1) &
        (param_sweep_df['timestep'] < 2) &
        (param_sweep_df['run'] == 1)
    ]
    return dataframe_difference(result_df, expected_df)

def test_timestep1psub0(Timestep1Psub0):
    compare_results_pytest(Timestep1Psub0)
