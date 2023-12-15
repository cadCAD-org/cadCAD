from testing.models import param_sweep
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
import pandas as pd # type: ignore
from testing.results_comparison import dataframe_difference, compare_results_pytest
import pytest


@pytest.fixture
def ParamSweep():
    exec_mode = ExecutionMode()
    exec_ctx = ExecutionContext(context=exec_mode.local_mode)
    run = Executor(exec_context=exec_ctx, configs=param_sweep.exp.configs)
    raw_result, _, _ = run.execute()

    result_df = pd.DataFrame(raw_result)
    expected_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
    result_diff = dataframe_difference(result_df, expected_df)
    return result_diff

def test_pytest_compare_results(ParamSweep):
    compare_results_pytest(ParamSweep)
