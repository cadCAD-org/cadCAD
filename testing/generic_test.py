import unittest
from parameterized import parameterized
from functools import reduce
from tabulate import tabulate
from testing.utils import generate_assertions_df

# ToDo: Exec Debug mode (*) for which state and policy updates are validated during runtime using `expected_results`
# EXAMPLE: ('state_test' T/F, 'policy_test' T/F)
# ToDo: (Sys Model Config) give `expected_results to` `Configuration` for Exec Debug mode (*)
# ToDo: (expected_results) Function to generate sys metrics keys using system model config
# ToDo: (expected_results) Function to generate target_vals given user input (apply fancy validation lib later on)


# ToDo: Use self.assertRaises(AssertionError)


def make_generic_test(params):
    class TestSequence(unittest.TestCase):
        @parameterized.expand(params)
        def test_validate_results(self, name, result_df, expected_reults, target_cols):
            # alt for (*) Exec Debug mode
            tested_df = generate_assertions_df(result_df, expected_reults, target_cols)
            erroneous = tested_df[(tested_df['test'] == False)]
            if erroneous.empty is False:
                for index, row in erroneous.iterrows():
                    expected = expected_reults[(row['run'], row['timestep'], row['substep'])]
                    unexpected = {k: expected[k] for k in expected if k in row and expected[k] != row[k]}
                    for key in unexpected.keys():
                        erroneous[f"invalid_{key}"] = unexpected[key]
                # etc.

                print()
                print(tabulate(erroneous, headers='keys', tablefmt='psql'))

            self.assertTrue(reduce(lambda a, b: a and b, tested_df['test']))

        # def etc.

    return TestSequence
