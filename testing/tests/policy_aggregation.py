import unittest
import pandas as pd
from testing.generic_test import make_generic_test
from testing.system_models.policy_aggregation import run

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
# df = generate_assertions_df(result, expected_results, ['policies', 's1'])
# print(tabulate(df, headers='keys', tablefmt='psql'))


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
