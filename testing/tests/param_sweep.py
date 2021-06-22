import unittest, pandas as pd
from tabulate import tabulate
from testing.models import param_sweep
from testing.results_comparison import dataframe_difference, compare_results
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=param_sweep.exp.configs)
raw_result, _, _ = run.execute()

result_df = pd.DataFrame(raw_result)
expected_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
result_diff = dataframe_difference(result_df, expected_df)
print(tabulate(result_diff, headers='keys', tablefmt='psql'))


class ParamSweepTest(compare_results(result_diff)):
    pass


if __name__ == '__main__':
    unittest.main()
