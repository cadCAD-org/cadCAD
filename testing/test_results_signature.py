from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import Executor, ExecutionContext, ExecutionMode
import pytest
import pandas as pd  # type: ignore
from typing import Dict, List

# (N_simulations, N_sweeps, N_runs, N_timesteps, N_substeps)


CONFIG_SIGNATURES_TO_TEST = [
    (1, 20, 5, 10, 5), (3, 3, 3, 3, 3), (1, 3, 3, 3, 3),
    (3, 1, 3, 3, 3), (1, 1, 3, 3, 3),
    (3, 3, 1, 3, 3), (1, 3, 1, 3, 3), (1, 1, 1, 3, 3)]


def run_experiment(exp: Experiment, mode: str) -> List[Dict]:
    exec_context = ExecutionContext(mode)
    executor = Executor(exec_context=exec_context, configs=exp.configs)
    (records, tensor_field, _) = executor.execute()
    return records


def create_experiments(N_simulations=3, N_sweeps=3, N_runs=3, N_timesteps=3, N_substeps=3) -> Experiment:

    INITIAL_STATE = {'varA': None}
    PSUBs = [{'policies': {}, 'variables': {}}] * N_substeps
    params = {'A': [None] * N_sweeps,
              'B': [None]}

    SIM_CONFIG = config_sim(
        {
            "N": N_runs,
            "T": range(N_timesteps),
            "M": params,  # Optional
        }
    )

    exp = Experiment()
    for i_sim in range(N_simulations):
        exp.append_model(
            sim_configs=SIM_CONFIG,
            initial_state=INITIAL_STATE,
            partial_state_update_blocks=PSUBs
        )
    return exp


def expected_rows(N_simulations, N_sweeps, N_runs, N_timesteps, N_substeps) -> int:
    return N_simulations * N_sweeps * N_runs * (N_timesteps * N_substeps + 1)


@pytest.mark.parametrize("N_sim,N_sw,N_r,N_t,N_s", CONFIG_SIGNATURES_TO_TEST)
def test_identifiers_value_counts_single(N_sim, N_sw, N_r, N_t, N_s):
    args = (N_sim, N_sw, N_r, N_t, N_s)
    results = run_experiment(create_experiments(*args), 'single_proc')
    df = pd.DataFrame(results).query("timestep > 0")
    assert len(set(df.timestep.value_counts().values)) == 1
    assert len(set(df.subset.value_counts().values)) == 1
    assert len(set(df.run.value_counts().values)) == 1


@pytest.mark.parametrize("N_sim,N_sw,N_r,N_t,N_s", CONFIG_SIGNATURES_TO_TEST[:-1])
def test_identifiers_value_counts_multi(N_sim, N_sw, N_r, N_t, N_s):
    args = (N_sim, N_sw, N_r, N_t, N_s)
    results = run_experiment(create_experiments(*args), 'multi_proc')
    df = pd.DataFrame(results).query("timestep > 0")
    assert len(set(df.timestep.value_counts().values)) == 1
    assert len(set(df.subset.value_counts().values)) == 1
    assert len(set(df.run.value_counts().values)) == 1
