import unittest
from pprint import pprint

from parameterized import parameterized
from functools import reduce

from tabulate import tabulate


def generate_assertions_df(df, expected_results, target_cols, evaluations):
    test_names = []
    for eval_f in evaluations:
        def wrapped_eval(a, b):
            try:
                return eval_f(a, b)
            except KeyError:
                return True

        test_name = f"{eval_f.__name__}_test"
        test_names.append(test_name)
        df[test_name] = df.apply(
            lambda x: wrapped_eval(
                x.filter(items=target_cols).to_dict(),
                expected_results[(x['subset'], x['run'], x['timestep'], x['substep'])]
            ),
            axis=1
        )

    return df, test_names


def make_generic_test(params):
    class TestSequence(unittest.TestCase):
        # pprint(params)

        def generic_test(self, tested_df, expected_reults, test_name):
            erroneous = tested_df[(tested_df[test_name] == False)]
            print(tabulate(tested_df, headers='keys', tablefmt='psql'))

            if erroneous.empty is False:  # Or Entire df IS NOT erroneous
                for index, row in erroneous.iterrows():
                    # expected = expected_reults[(row['simulation'], row['run'], row['timestep'], row['substep'])]
                    expected = expected_reults[(row['subset'], row['run'], row['timestep'], row['substep'])]
                    unexpected = {f"invalid_{k}": expected[k] for k in expected if k in row and expected[k] != row[k]}

                    for key in unexpected.keys():
                        erroneous[key] = None
                        erroneous.at[index, key] = unexpected[key]
                # etc.

            self.assertTrue(reduce(lambda a, b: a and b, tested_df[test_name]))

        @parameterized.expand(params)
        def test_validation(self, name, result_df, expected_results, target_cols, evaluations):
            tested_df, test_names = generate_assertions_df(result_df, expected_results, target_cols, evaluations)

            for test_name in test_names:
                self.generic_test(tested_df, expected_results, test_name)

    return TestSequence
