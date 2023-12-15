import pandas as pd
from tabulate import tabulate
from testing.results_comparison import dataframe_difference, compare_results_pytest
from cadCAD import configs
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
import pytest


@pytest.fixture
def empty_experiment():
    exec_mode = ExecutionMode()
    exec_ctx = ExecutionContext(context=exec_mode.local_mode)
    run = Executor(exec_context=exec_ctx, configs=configs)
    raw_result, _, _ = run.execute()

    result_df = pd.DataFrame(raw_result)
    expected_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
    return dataframe_difference(result_df, expected_df)


def test_experiment(empty_experiment):
    compare_results_pytest(empty_experiment)
