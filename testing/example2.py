from functools import reduce

import pandas as pd
import unittest
from parameterized import parameterized
from tabulate import tabulate

from testing.system_models.policy_aggregation import run
from testing.generic_test import make_generic_test
from testing.utils import generate_assertions_df

raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)

expected_results = {
    (1, 0, 0): {'policies': {}, 's1': 0},
    (1, 1, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 500},
    (1, 1, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 2},
    (1, 1, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 3},
    (1, 2, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 4},
    (1, 2, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 5},
    (1, 2, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 6},
    (1, 3, 1): {'policies': {'policy1': 2, 'policy2': 4}, 's1': 7},
    (1, 3, 2): {'policies': {'policy1': 8, 'policy2': 8}, 's1': 8},
    (1, 3, 3): {'policies': {'policy1': 4, 'policy2': 8, 'policy3': 12}, 's1': 9}
}

params = [["policy_aggregation", result, expected_results, ['policies', 's1']]]


class TestSequence(unittest.TestCase):
    @parameterized.expand(params)
    def test_validate_results(self, name, result_df, expected_reults, target_cols):
        # alt for (*) Exec Debug mode
        tested_df = generate_assertions_df(result_df, expected_reults, target_cols)

        erroneous = tested_df[(tested_df['test'] == False)]
        for index, row in erroneous.iterrows():
            expected = expected_reults[(row['run'], row['timestep'], row['substep'])]
            unexpected = {k: expected[k] for k in expected if k in row and expected[k] != row[k]}
            for key in unexpected.keys():
                erroneous[f"invalid_{key}"] = unexpected[key]
        # etc.

        # def etc.

        print()
        print(tabulate(erroneous, headers='keys', tablefmt='psql'))

        self.assertEqual(reduce(lambda a, b: a and b, tested_df['test']), True)

        s = 'hello world'
        # self.assertEqual(s.split(), 1)
        # # check that s.split fails when the separator is not a string
        # with self.assertRaises(AssertionError):
        #     tested_df[(tested_df['test'] == False)]
        #     erroneous = tested_df[(tested_df['test'] == False)]
        #     for index, row in erroneous.iterrows():
        #         expected = expected_reults[(row['run'], row['timestep'], row['substep'])]
        #         unexpected = {k: expected[k] for k in expected if k in row and expected[k] != row[k]}
        #         for key in unexpected.keys():
        #             erroneous[f"invalid_{key}"] = unexpected[key]
        #     # etc.
        #
        #     # def etc.
        #
        #     print()
        #     print(tabulate(erroneous, headers='keys', tablefmt='psql'))

if __name__ == '__main__':
    unittest.main()