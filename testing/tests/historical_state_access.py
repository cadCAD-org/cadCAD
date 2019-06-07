import unittest
import pandas as pd
from tabulate import tabulate

from testing.generic_test import make_generic_test
from testing.system_models.historical_state_access import run
from testing.utils import generate_assertions_df

raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)

expected_results = {
    (1, 0, 0): {'x': 0, 'nonexsistant': [], 'last_x': [], '2nd_to_last_x': [], '3rd_to_last_x': [], '4th_to_last_x': []},
    (1, 1, 1): {'x': 1,
                'nonexsistant': [],
                'last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 1, 2): {'x': 2,
                'nonexsistant': [],
                'last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 1, 3): {'x': 3,
                'nonexsistant': [],
                'last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 2, 1): {'x': 4,
                'nonexsistant': [],
                'last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '2nd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 2, 2): {'x': 5,
                'nonexsistant': [],
                'last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '2nd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 2, 3): {'x': 6,
                'nonexsistant': [],
                'last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '2nd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (1, 3, 1): {'x': 7,
                'nonexsistant': [],
                'last_x': [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}],
                '2nd_to_last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '3rd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []},
    (1, 3, 2): {'x': 8,
                'nonexsistant': [],
                'last_x': [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}],
                '2nd_to_last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '3rd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []},
    (1, 3, 3): {'x': 9,
                'nonexsistant': [],
                'last_x': [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}],
                '2nd_to_last_x': [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}],
                '3rd_to_last_x': [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []}
}

params = [["historical_state_access", result, expected_results,
           ['x', 'nonexsistant', 'last_x', '2nd_to_last_x', '3rd_to_last_x', '4th_to_last_x']]
          ]
# df = generate_assertions_df(result, expected_results,
#                             ['x', 'nonexsistant', 'last_x', '2nd_to_last_x', '3rd_to_last_x', '4th_to_last_x']
#                             )
# print(tabulate(df, headers='keys', tablefmt='psql'))


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
