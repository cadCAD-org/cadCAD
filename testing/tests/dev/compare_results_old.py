from copy import deepcopy

import pandas as pd
import numpy as np
# import pandasql
# from tabulate import tabulate
from tabulate import tabulate

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.models import param_sweep

exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.local_mode)
run = Executor(exec_context=exec_ctx, configs=param_sweep.exp.configs)

raw_result, tensor_fields, sessions = run.execute()
result = pd.DataFrame(raw_result)
# print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
# pprint(sessions)
# print(tabulate(result, headers='keys', tablefmt='psql'))

# result_1 = result
# result_2 = deepcopy(result)

# test_df1 = pd.testing.assert_frame_equal(result_1, result_2)
# print(tabulate(test_df1, headers='keys', tablefmt='psql'))

result_df = pd.DataFrame({'a': [1, 2], 'b': [3, 5]}).reset_index()
df2 = pd.DataFrame({'a': [3.1, 2], 'b': [3.0, 4.0]}).reset_index()

# test_df2 = pd.testing.assert_frame_equal(df1, df2)
# print(tabulate(test_df2, headers='keys', tablefmt='psql'))

def dataframe_difference(df1: pd.DataFrame, df2: pd.DataFrame, which=None):
    """
        Find rows which are different between two DataFrames.
        https://hackersandslackers.com/compare-rows-pandas-dataframes/
    """
    comparison_df = df1.merge(
        df2,
        indicator=True,
        how='outer'
    )
    if which is None:
        diff_df = comparison_df[comparison_df['_merge'] != 'both']
    else:
        diff_df = comparison_df[comparison_df['_merge'] == which]
    # diff_df.to_csv('data/diff.csv')
    return diff_df


merge_df = dataframe_difference(result_df, df2)
cols_no__merge = list(filter(lambda col: '_merge' not in col, merge_df.columns.tolist()))
cols_no_index = list(filter(lambda col: 'index' not in col, cols_no__merge))
aggregation = dict((k, 'unique') for k in cols_no_index)
diff_df = merge_df[cols_no__merge].groupby('index').agg(aggregation)
# print(tabulate(diff_df, headers='keys', tablefmt='psql'))


def discrepancies(row):
    return dict([
        (col, list(vals)) for col, vals in row.items()
            if type(vals) is np.ndarray and len(vals) > 1
    ])


def val_error(val):
    if type(val) is dict:
        return False
    else:
        return True


diff_df['discrepancies'] = diff_df.apply(discrepancies, axis=1)
discrepancies_df = diff_df[['discrepancies']]
result_diff = result_df.merge(discrepancies_df, how='left', on='index')
result_diff['val_error'] = result_diff['discrepancies'].apply(val_error)
print(tabulate(result_diff, headers='keys', tablefmt='psql'))

