from typing import Dict, List, Optional
from cadCAD.engine import Executor, ExecutionContext, ExecutionMode
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import env_trigger, var_substep_trigger, config_sim, psub_list
from cadCAD.types import *
import pandas as pd  # type: ignore
import types
import inspect
import pytest
from pandas import DataFrame


def describe_or_return(v: object) -> object:
    """
    Thanks @LinuxIsCool!
    """
    if isinstance(v, types.FunctionType):
        return f'function: {v.__name__}'
    elif isinstance(v, types.LambdaType) and v.__name__ == '<lambda>':
        return f'lambda: {inspect.signature(v)}'
    else:
        return v


def select_M_dict(M_dict: Dict[str, object], keys: set) -> Dict[str, object]:
    """
    Thanks @LinuxIsCool!
    """
    return {k: describe_or_return(v) for k, v in M_dict.items() if k in keys}


def select_config_M_dict(configs: list, i: int, keys: set) -> Dict[str, object]:
    return select_M_dict(configs[i].sim_config['M'], keys)


def drop_substeps(_df):
    first_ind = (_df.substep == 0) & (_df.timestep == 0)
    last_ind = _df.substep == max(_df.substep)
    inds_to_drop = first_ind | last_ind
    return _df.copy().loc[inds_to_drop].drop(columns=['substep'])


def assign_params(_df: pd.DataFrame, configs) -> pd.DataFrame:
    """
    Based on `cadCAD-tools` package codebase, by @danlessa
    """
    M_dict = configs[0].sim_config['M']
    params_set = set(M_dict.keys())
    selected_params = params_set

    # Attribute parameters to each row
    # 1. Assign the parameter set from the first row first, so that
    # columns are created
    first_param_dict = select_config_M_dict(configs, 0, selected_params)

    # 2. Attribute parameter on an (simulation, subset, run) basis
    df = _df.assign(**first_param_dict).copy()
    for i, (_, subset_df) in enumerate(df.groupby(['simulation', 'subset', 'run'])):
        df.loc[subset_df.index] = subset_df.assign(**select_config_M_dict(configs,
                                                                          i,
                                                                          selected_params))
    return df


SWEEP_PARAMS: Dict[str, List] = {
    'alpha': [1],
    'beta': [lambda x: 2 * x, lambda x: x, lambda x: x / 2],
    'gamma': [3, 4, 5],
    'omega': [7]
}

SINGLE_PARAMS: Dict[str, object] = {
    'alpha': 1,
    'beta': lambda x: x,
    'gamma': 3,
    'omega': 5
}


def create_experiment(N_RUNS=2, N_TIMESTEPS=3, params: dict = SWEEP_PARAMS):
    psu_steps = ['m1', 'm2', 'm3']
    system_substeps = len(psu_steps)
    var_timestep_trigger = var_substep_trigger([0, system_substeps])
    env_timestep_trigger = env_trigger(system_substeps)
    env_process = {}

    # ['s1', 's2', 's3', 's4']
    # Policies per Mechanism

    def gamma(params: Parameters, substep: Substep, history: StateHistory, state: State, **kwargs):
        return {'gamma': params['gamma']}

    def omega(params: Parameters, substep: Substep, history: StateHistory, state: State, **kwarg):
        return {'omega': params['omega']}

    # Internal States per Mechanism

    def alpha(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'alpha_var', params['alpha']

    def beta(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'beta_var', params['beta']

    def gamma_var(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'gamma_var', params['gamma']

    def omega_var(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'omega_var', params['omega']

    def policies(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'policies', _input

    def sweeped(params: Parameters, substep: Substep, history: StateHistory, state: State, _input: PolicyOutput, **kwargs):
        return 'sweeped', {'beta': params['beta'], 'gamma': params['gamma']}

    psu_block: dict = {k: {"policies": {}, "states": {}} for k in psu_steps}
    for m in psu_steps:
        psu_block[m]['policies']['gamma'] = gamma
        psu_block[m]['policies']['omega'] = omega
        psu_block[m]["states"]['alpha_var'] = alpha
        psu_block[m]["states"]['beta_var'] = beta
        psu_block[m]["states"]['gamma_var'] = gamma_var
        psu_block[m]["states"]['omega_var'] = omega_var
        psu_block[m]['states']['policies'] = policies
        psu_block[m]["states"]['sweeped'] = var_timestep_trigger(
            y='sweeped', f=sweeped)

    # Genesis States
    genesis_states = {
        'alpha_var': 0,
        'beta_var': 0,
        'gamma_var': 0,
        'omega_var': 0,
        'policies': {},
        'sweeped': {}
    }

    # Environment Process
    env_process['sweeped'] = env_timestep_trigger(trigger_field='timestep', trigger_vals=[
                                                  5], funct_list=[lambda _g, x: _g['beta']])

    sim_config = config_sim(
        {
            "N": N_RUNS,
            "T": range(N_TIMESTEPS),
            "M": params,  # Optional
        }
    )

    # New Convention
    partial_state_update_blocks = psub_list(psu_block, psu_steps)

    exp = Experiment()
    exp.append_model(
        sim_configs=sim_config,
        initial_state=genesis_states,
        env_processes=env_process,
        partial_state_update_blocks=partial_state_update_blocks
    )
    return exp

@pytest.mark.parametrize("mode", ["local_proc", "single_proc", "multi_proc"])
def test_mc_sweep_experiment(mode):
    experiment_assertions(create_experiment(
        N_RUNS=2, N_TIMESTEPS=2, params=SWEEP_PARAMS), mode)

@pytest.mark.parametrize("mode", ["local_proc", "single_proc", "multi_proc"])
def test_unique_sweep_experiment(mode):
    experiment_assertions(create_experiment(
        N_RUNS=1, N_TIMESTEPS=2, params=SWEEP_PARAMS), mode)

@pytest.mark.parametrize("mode", ["local_proc", "single_proc", "multi_proc"])
def test_mc_single_experiment(mode):
    experiment_assertions(create_experiment(
        N_RUNS=2, N_TIMESTEPS=2, params=SINGLE_PARAMS), mode)

@pytest.mark.parametrize("mode", ["local_proc", "single_proc", "multi_proc"])
def test_unique_single_experiment(mode):
    if mode == "multi_proc":
            with pytest.raises(ValueError) as e_info:
                experiment_assertions(create_experiment(
                    N_RUNS=1, N_TIMESTEPS=2, params=SINGLE_PARAMS), mode)
    else:
        experiment_assertions(create_experiment(
                    N_RUNS=1, N_TIMESTEPS=2, params=SINGLE_PARAMS), mode)


def experiment_assertions(exp: Experiment, mode: Optional[str]=None) -> None:
    if mode == None:
        mode = ExecutionMode().local_mode
    exec_context = ExecutionContext(mode)
    executor = Executor(exec_context=exec_context, configs=exp.configs)
    (records, tensor_field, _) = executor.execute()

    df: DataFrame = assign_params(pd.DataFrame(records), exp.configs)
    df = drop_substeps(df)

    # XXX: parameters should always be of the same type. Else, the test will fail
    first_sim_config = exp.configs[0].sim_config['M']

    required_keys = {'simulation': int,
                     'run': int,
                     'subset': int,
                     'timestep': int}

    for (i, row) in df.iterrows():
        if row.timestep > 0:

            assert row['alpha_var'] == row['alpha']
            assert type(row['alpha_var']) == type(first_sim_config['alpha'])
            assert row['gamma_var'] == row['gamma']
            assert type(row['gamma_var']) == type(first_sim_config['gamma'])
            assert row['omega_var'] == row['omega']
            assert type(row['omega_var']) == type(first_sim_config['omega'])
            for k, v in required_keys.items():
                assert k in row
                assert type(row[k]) == v
