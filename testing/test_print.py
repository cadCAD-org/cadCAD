from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import Executor, ExecutionContext, ExecutionMode
import pytest

P_no_lst = {'pA': 1, 'pB': 2, 'pC': 3}
P_single_lst = {'pA': [1], 'pB': [1], 'pC': [3]}
P_single_swp = {'pA': [4, 5, 6], 'pB': [1], 'pC': [3]}
P_all_swp = {'pA': [7, 8, 9], 'pB': [1, 2, 3], 'pC': [1, 2, 3]}
P_all_but_one_swp = {'pA': [7, 8, 9], 'pB': [1, 2, 3], 'pC': [1]}
Ps = [P_no_lst, P_single_lst, P_single_swp, P_all_swp, P_all_but_one_swp]

CONFIG_SIGNATURES_TO_TEST = [(3, 3, 3, 3, 3),
                             (1, 3, 3, 3, 3),
                             (3, 1, 3, 3, 3),
                             (1, 1, 3, 3, 3),
                             (3, 3, 1, 3, 3),
                             (1, 3, 1, 3, 3),
                             (1, 1, 1, 3, 3)]


def run_experiment(exp: Experiment, mode: str, supress_print=False):
    exec_context = ExecutionContext(mode)
    executor = Executor(exec_context=exec_context, configs=exp.configs, supress_print=supress_print)
    (records, tensor_field, _) = executor.execute()
    return records


def param_count_test_suf_generator(provided_params):
    def s_test_param_count(params, _2, _3, _4, _5):
        assert params.keys() == provided_params.keys(), 'Params are not matching'
        return ('varA', None)
    return s_test_param_count


def param_count_test_policy_generator(provided_params):
    def p_test_param_count(params, _2, _3, _4):
        assert params.keys() == provided_params.keys(), 'Params are not matching'
        return {'sigA': None}
    return p_test_param_count


def create_experiments(N_simulations=3, N_sweeps=3, N_runs=3, N_timesteps=3, N_substeps=3, params={}) -> Experiment:

    INITIAL_STATE = {'varA': None}
    PSUBs = [{'policies': {'sigA': param_count_test_policy_generator(
        params)}, 'variables': {'varA': param_count_test_suf_generator(params)}}] * N_substeps

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



def test_print(capfd):
    exp = run_experiment(create_experiments(N_simulations=3, N_sweeps=3, N_runs=3, N_timesteps=3, N_substeps=3, params={'a': 0}), 'single_proc', supress_print=False)
    out, err = capfd.readouterr()
    assert "                  ___________    ____\n  ________ __ ___/ / ____/   |  / __ \\\n / ___/ __` / __  / /   / /| | / / / /\n/ /__/ /_/ / /_/ / /___/ ___ |/ /_/ /\n\\___/\\__,_/\\__,_/\\____/_/  |_/_____/\nby cadCAD" in out
    assert 'Initializing configurations' in err

    exp = run_experiment(create_experiments(N_simulations=3, N_sweeps=3, N_runs=3, N_timesteps=3, N_substeps=3, params={'a': 0}), 'single_proc', supress_print=True)
    out, err = capfd.readouterr()
    assert out == ''
    assert err == ''