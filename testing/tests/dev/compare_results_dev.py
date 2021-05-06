import unittest
import pandas as pd
from copy import deepcopy

from testing.models import param_sweep
from testing.results_comparison import dataframe_difference, compare_results
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=param_sweep.exp.configs)

raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
# print(tabulate(result, headers='keys', tablefmt='psql'))


result_1 = result
result_2 = deepcopy(result)
result_df1 = pd.DataFrame({'a': [1, 2], 'b': [3, 5]})
result_df2 = pd.DataFrame({'a': ['hi', 2], 'b': [3.0, 4.0]})

# print(result_df1.shape)
# exit()



equivalent_result_diff = dataframe_difference(result_1, result_2)
different_result_diff = dataframe_difference(result_df1, result_df2)

class dfCompareTest(compare_results(different_result_diff)):
    pass

class EquivalentTest(compare_results(equivalent_result_diff)):
    pass

if __name__ == '__main__':
    unittest.main()
