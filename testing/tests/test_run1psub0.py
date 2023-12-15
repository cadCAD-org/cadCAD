import pandas as pd # type: ignore
from testing.results_comparison import dataframe_difference, compare_results_pytest
import pytest


@pytest.fixture
def Run1Psub0():
    expected_df = pd.read_pickle("expected_results/param_sweep_psub0_4.pkl")
    param_sweep_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
    result_df = param_sweep_df[
        (param_sweep_df.index > 0) & (param_sweep_df['subset'] < 1) & (param_sweep_df['run'] == 1)
    ]
    result_diff = dataframe_difference(result_df, expected_df)
    return result_diff

def test_pytest_compare_results(Run1Psub0):
    compare_results_pytest(Run1Psub0)

