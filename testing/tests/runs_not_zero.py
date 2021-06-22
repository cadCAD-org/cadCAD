import unittest
from cadCAD.configuration.utils import config_sim

val_error_indicator = False
try:
    sim_config = config_sim(
        {
            "N": 0,
            "T": range(5)
        }
    )
except ValueError:
    val_error_indicator = True


class RunExceptionTest(unittest.TestCase):
    def test_multi_model(self):
        self.assertEqual(val_error_indicator, True, "ValueError raised when runs (N) < 1")


if __name__ == '__main__':
    unittest.main()
