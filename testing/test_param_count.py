from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import Executor, ExecutionContext, ExecutionMode
import pytest




P_no_lst = {'pA': 1, 'pB': 2, 'pC': 3}
P_single_lst = {'pA': [1], 'pB': [1], 'pC': [3]}
P_single_swp = {'pA': [1, 2, 3], 'pB': [1], 'pC': [3]}
P_all_swp = {'pA': [1, 2, 3], 'pB': [1, 2, 3], 'pC': [1, 2, 3]}
Ps = [P_no_lst, P_single_lst, P_single_swp, P_all_swp]

CONFIG_SIGNATURES_TO_TEST = [(3, 3, 3, 3, 3), (1, 3, 3, 3, 3),
 (3, 1, 3, 3, 3), (1, 1, 3, 3, 3),
 (3, 3, 1, 3, 3), (1, 3, 1, 3, 3), (1, 1, 1, 3, 3)]


def run_experiment(exp: Experiment, mode: str):
    exec_context = ExecutionContext(mode)
    executor = Executor(exec_context=exec_context, configs=exp.configs)
    (records, tensor_field, _) = executor.execute()
    return records






def param_count_test_generator(provided_params):
    def s_test_param_count(params, _2, _3, _4, _5):
        assert params.keys() == provided_params.keys()


def create_experiments(N_simulations=3, N_sweeps=3, N_runs=3, N_timesteps=3, N_substeps=3, params={}) -> Experiment:

    INITIAL_STATE = {'varA': None}
    PSUBs = [{'policies': {}, 'variables': {'varA': param_count_test_generator(params)}}] * N_substeps

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


def expected_rows(N_simulations, N_sweeps, N_runs, N_timesteps, N_substeps,P) -> int:
    return N_simulations * N_sweeps *  N_runs * (N_timesteps * N_substeps + 1)


@pytest.mark.parametrize("N_sim,N_sw,N_r,N_t,N_s", CONFIG_SIGNATURES_TO_TEST)
@pytest.mark.parametrize("P", Ps)
def test_row_count_single(N_sim, N_sw, N_r, N_t, N_s, P):
    args = (N_sim, N_sw, N_r, N_t, N_s, P)
    assert len(run_experiment(create_experiments(*args), 'single_proc')) == expected_rows(*args)


@pytest.mark.parametrize("N_sim,N_sw,N_r,N_t,N_s", CONFIG_SIGNATURES_TO_TEST)
@pytest.mark.parametrize("P", Ps)
def test_row_count_multi(N_sim, N_sw, N_r, N_t, N_s, P):
    args = (N_sim, N_sw, N_r, N_t, N_s, P)

    if N_sim == 1 and N_sw == 1 and N_r == 1:
        with pytest.raises(ValueError) as e_info:
            assert len(run_experiment(create_experiments(*args), 'multi_proc')) == expected_rows(*args)
    else:
        assert len(run_experiment(create_experiments(*args), 'multi_proc')) == expected_rows(*args)


@pytest.mark.parametrize("N_sim,N_sw,N_r,N_t,N_s", CONFIG_SIGNATURES_TO_TEST)
@pytest.mark.parametrize("P", Ps)
def test_row_count_local(N_sim, N_sw, N_r, N_t, N_s, P):
    args = (N_sim, N_sw, N_r, N_t, N_s, P)
    assert len(run_experiment(create_experiments(*args), 'local_proc')) == expected_rows(*args)
