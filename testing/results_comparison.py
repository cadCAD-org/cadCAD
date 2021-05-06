import unittest
import pandas as pd
from tabulate import tabulate
from pandas._testing import assert_frame_equal


def compare_results(result_diff):
    class CompareResults(unittest.TestCase):
        def setUp(self):
            result_diff.columns
            self.val_error_status_ind = False not in result_diff.val_error_status.tolist()
            self.type_error_status_ind = False not in result_diff.type_error_status.tolist()
            self.df_out = None
            self.erroneous_indexes = None
            self.select_result_diff = None

            if (self.val_error_status_ind is False) or (self.type_error_status_ind is False):
                self.erroneous_indexes = list(result_diff.index[result_diff["val_error_status"] == False])
                self.select_result_diff = result_diff.iloc[self.erroneous_indexes]
                self.df_out = tabulate(self.select_result_diff, headers='keys', tablefmt='psql')

        def test_val_error_status(self):
            print(self.df_out)
            self.assertEqual(self.val_error_status_ind, True, "Value Error")

        def test_type_error_status(self):
            print(self.df_out)
            self.assertEqual(self.type_error_status_ind, True, "Type Error")

    return CompareResults


def dataframe_difference(df1, df2):
    def discrepancies(row):
        return {
            col: {'values': list(vals), 'type': [type(v) for v in vals]} for col, vals in row.items()
            if vals[0] != vals[1]
        }

    def val_error_status(val):
        if type(val) is dict and len(val) != 0:
            return False
        else:
            return True

    def type_error_status(val):
        if type(val) is dict and len(val) != 0:
            return list(set([v['type'][0] == v['type'][1] for k, v in val.items()]))[0]
        else:
            return True

    df1_cols, df2_cols = list(df1.columns), list(df2.columns)
    if set(df1_cols) == set(df2_cols) and df1.shape == df2.shape:
        df_equal_ind = True
        try:
            assert_frame_equal(df1, df2)
        except:
            df_equal_ind = False

        if df_equal_ind is False:
            data = [list(zip(df1[col], df2[col])) for col in df1_cols]

            df = pd.DataFrame(data).T
            df.columns = df1_cols
            df['discrepancies'] = df.apply(discrepancies, axis=1)

            result_df1 = df1.reset_index()
            discrepancies_df = df[['discrepancies']].reset_index()
            result_diff = result_df1.merge(discrepancies_df, how='left', on='index')
            result_diff['val_error_status'] = result_diff['discrepancies'].apply(val_error_status)
            result_diff['type_error_status'] = result_diff['discrepancies'].apply(type_error_status)

            return result_diff
        else:
            df1['discrepancies'] = None
            df1['val_error_status'] = True
            df1['type_error_status'] = True
            return df1
    else:
        df1_row_count, df1_col_count = df1.shape
        df2_row_count, df2_col_count = df2.shape
        raise Exception(f"""
        DataFrames have mismatched dimensions or columns:

            Columns:
                * df1: {df1_cols}
                * df2: {df2_cols}     
            Shapes:
                * df1: 
                    *    Row Count: {df1_row_count}
                    * Column Count: {df1_col_count}
                * df2:
                    *    Row Count: {df2_row_count}
                    * Column Count: {df2_col_count}
        """)
