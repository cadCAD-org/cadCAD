import unittest
import pandas as pd

from cadCAD import configs
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.generic_test import make_generic_test

exec_mode = ExecutionMode()
exec_ctx = ExecutionContext(context=exec_mode.single_mode)
run = Executor(exec_context=exec_ctx, configs=configs)

raw_result, tensor_field, _ = run.execute()
result = pd.DataFrame(raw_result)
expected_results = {
    (0, 1, 0, 0): {'x': 0, 'nonexsistant': [], 'last_x': [], '2nd_to_last_x': [], '3rd_to_last_x': [], '4th_to_last_x': []},
    (0, 1, 1, 1): {'x': 1,
                'nonexsistant': [],
                'last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 1, 2): {'x': 2,
                'nonexsistant': [],
                'last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 1, 3): {'x': 3,
                'nonexsistant': [],
                'last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '2nd_to_last_x': [],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 2, 1): {'x': 4,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '2nd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 2, 2): {'x': 5,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '2nd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 2, 3): {'x': 6,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '2nd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '3rd_to_last_x': [],
                '4th_to_last_x': []},
    (0, 1, 3, 1): {'x': 7,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 4, 'run': 1, 'substep': 1, 'timestep': 2},
                    {'simulation': 0, 'x': 5, 'run': 1, 'substep': 2, 'timestep': 2},
                    {'simulation': 0, 'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}
                ],
                '2nd_to_last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '3rd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []},
    (0, 1, 3, 2): {'x': 8,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 4, 'run': 1, 'substep': 1, 'timestep': 2},
                    {'simulation': 0, 'x': 5, 'run': 1, 'substep': 2, 'timestep': 2},
                    {'simulation': 0, 'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}
                ],
                '2nd_to_last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '3rd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []},
    (0, 1, 3, 3): {'x': 9,
                'nonexsistant': [],
                'last_x': [
                    {'simulation': 0, 'x': 4, 'run': 1, 'substep': 1, 'timestep': 2},
                    {'simulation': 0, 'x': 5, 'run': 1, 'substep': 2, 'timestep': 2},
                    {'simulation': 0, 'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}
                ],
                '2nd_to_last_x': [
                    {'simulation': 0, 'x': 1, 'run': 1, 'substep': 1, 'timestep': 1},
                    {'simulation': 0, 'x': 2, 'run': 1, 'substep': 2, 'timestep': 1},
                    {'simulation': 0, 'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}
                ],
                '3rd_to_last_x': [{'simulation': 0, 'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}],
                '4th_to_last_x': []}
}


def row(a, b):
    return a == b
params = [
    ["historical_state_access", result, expected_results,
           ['x', 'nonexsistant', 'last_x', '2nd_to_last_x', '3rd_to_last_x', '4th_to_last_x'], [row]]
    ]


class GenericTest(make_generic_test(params)):
    pass


if __name__ == '__main__':
    unittest.main()
