from cadCAD.types import *
import pandas as pd


def generic_suf(variable: str, signal: str = "") -> StateUpdateFunction:
    """
    Generate a State Update Function that assigns the signal value to the
    given variable. By default, the signal has the same identifier as the
    variable.
    """
    if signal is "":
        signal = variable
    else:
        pass

    def suf(_1, _2, _3, _4, signals: PolicyOutput) -> StateUpdateTuple:
        return (variable, signals[signal])

    return suf


def add_parameter_labels(configs: list, df: pd.DataFrame) -> pd.DataFrame:
    """Utility function to add the parameters to a dataframe after processing

    Args:
        configs (list): The configurations of the simulations
        df (pd.DataFrame): Simulation dataframe

    Returns:
        pd.DataFrame: Simulation dataframe with labels
    """

    # Find the relevant parameters
    sim_params = pd.DataFrame([x.sim_config["M"] for x in configs])
    sim_params[["subset", "simulation", "run"]] = [
        [x.subset_id, x.simulation_id, x.run_id] for x in configs
    ]
    # Fix because run_id is 0 indexed, but cadCAD dataframe is 1 indexed for runs
    sim_params["run"] += 1

    # Join
    sim_params = sim_params.set_index(["subset", "simulation", "run"])
    df = df.join(sim_params, on=["subset", "simulation", "run"])
    return df
