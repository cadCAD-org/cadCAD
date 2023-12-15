from cadCAD.configuration.utils import config_sim
from testing.utils import assertEqual

def test_runs_not_zero():
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
    assertEqual(val_error_indicator, True, "ValueError raised when runs (N) < 1")
