import json
import os
import pandas as pd # type: ignore
from cadCAD.configuration import Experiment
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from testing.models import param_sweep, policy_aggregation
import pytest
from dataclasses import dataclass
from testing.utils import assertEqual

@dataclass
class MultiModelRowCountResults():
    expected_rows: object
    expected_rows_from_api: object
    result_rows: object
    param_sweep_df_rows: object
    policy_agg_df_rows: object
    sys_model_A_id: object
    sys_model_B_id: object
    sys_model_C_id: object
    model_A_rows: object
    model_B_rows: object
    model_C_rows: object

@pytest.fixture
def multi_model_row_count():
    exp = Experiment()
    sys_model_A_id = "sys_model_A"
    exp.append_model(
        model_id=sys_model_A_id,
        sim_configs=param_sweep.sim_config,
        initial_state=param_sweep.genesis_states,
        env_processes=param_sweep.env_process,
        partial_state_update_blocks=param_sweep.partial_state_update_blocks
    )
    sys_model_B_id = "sys_model_B"
    exp.append_model(
        model_id=sys_model_B_id,
        sim_configs=param_sweep.sim_config,
        initial_state=param_sweep.genesis_states,
        env_processes=param_sweep.env_process,
        partial_state_update_blocks=param_sweep.partial_state_update_blocks
    )
    sys_model_C_id = "sys_model_C"
    exp.append_model(
        model_id=sys_model_C_id,
        sim_configs=policy_aggregation.sim_config,
        initial_state=policy_aggregation.genesis_states,
        partial_state_update_blocks=policy_aggregation.partial_state_update_block,
        policy_ops=[lambda a, b: a + b, lambda y: y * 2] # Default: lambda a, b: a + b
    )

    simulation = 3
    model_A_sweeps = len(param_sweep.sim_config)
    model_B_sweeps = len(param_sweep.sim_config)
    model_C_sweeps = 1
    # total_sweeps = model_A_sweeps + model_B_sweeps

    model_A_runs = param_sweep.sim_config[0]['N']
    model_B_runs = param_sweep.sim_config[0]['N']
    model_C_runs = policy_aggregation.sim_config['N']
    # total_runs = model_A_runs + model_B_runs

    model_A_timesteps = len(param_sweep.sim_config[0]['T'])
    model_B_timesteps = len(param_sweep.sim_config[0]['T'])
    model_C_timesteps = len(policy_aggregation.sim_config['T'])

    model_A_substeps = len(param_sweep.partial_state_update_blocks)
    model_B_substeps = len(param_sweep.partial_state_update_blocks)
    model_C_substeps = len(policy_aggregation.partial_state_update_block)
    # total_substeps = model_A_substeps + model_B_substeps

    model_A_init_rows = model_A_runs * model_A_sweeps
    model_B_init_rows = model_B_runs * model_B_sweeps
    model_C_init_rows = model_C_runs * 1
    model_A_rows = model_A_init_rows + (model_A_sweeps * (model_A_runs * model_A_timesteps * model_A_substeps))
    model_B_rows = model_B_init_rows + (model_B_sweeps * (model_B_runs * model_B_timesteps * model_B_substeps))
    model_C_rows = model_C_init_rows + (model_C_sweeps * (model_C_runs * model_C_timesteps * model_C_substeps))


    exec_mode = ExecutionMode()
    local_mode_ctx = ExecutionContext(context=exec_mode.local_mode)
    simulation = Executor(exec_context=local_mode_ctx, configs=exp.configs)
    raw_results, _, _ = simulation.execute()

    results_df = pd.DataFrame(raw_results)
    param_sweep_df = pd.read_pickle("expected_results/param_sweep_4.pkl")
    policy_agg_df = pd.read_pickle("expected_results/policy_agg_4.pkl")
    param_sweep_df_rows = len(param_sweep_df.index)
    policy_agg_df_rows = len(policy_agg_df.index)

    expected_rows = param_sweep_df_rows + param_sweep_df_rows + policy_agg_df_rows
    expected_rows_from_api = model_A_rows + model_B_rows + model_C_rows
    result_rows = len(results_df.index)
    return MultiModelRowCountResults(expected_rows,
                                     expected_rows_from_api,
                                     result_rows,
                                     param_sweep_df_rows,
                                     policy_agg_df_rows,
                                     sys_model_A_id,
                                     sys_model_B_id,
                                     sys_model_C_id,
                                     model_A_rows,
                                     model_B_rows,
                                     model_C_rows)


def test_row_count(multi_model_row_count: MultiModelRowCountResults):
    equal_row_count = multi_model_row_count.expected_rows == multi_model_row_count.expected_rows_from_api == multi_model_row_count.result_rows
    assertEqual(equal_row_count, True, "Row Count Mismatch between Expected and Multi-Model simulation results")

    
def test_row_count_from_api(multi_model_row_count: MultiModelRowCountResults):
    assertEqual(multi_model_row_count.expected_rows == multi_model_row_count.expected_rows_from_api, True, "API not producing Expected simulation results")

    
def test_row_count_from_results(multi_model_row_count: MultiModelRowCountResults):
    assertEqual(multi_model_row_count.expected_rows == multi_model_row_count.result_rows, True, "Engine not producing Expected simulation results")

    
def test_row_count_from_sys_model_A(multi_model_row_count: MultiModelRowCountResults):
    assertEqual(multi_model_row_count.model_A_rows == multi_model_row_count.param_sweep_df_rows, True, f"{multi_model_row_count.sys_model_A_id}: Row Count Mismatch with Expected results")

    
def test_row_count_from_sys_model_B(multi_model_row_count: MultiModelRowCountResults):
    assertEqual(multi_model_row_count.model_B_rows == multi_model_row_count.param_sweep_df_rows, True, f"{multi_model_row_count.sys_model_B_id}: Row Count Mismatch with Expected results")

    
def test_row_count_from_sys_model_C(multi_model_row_count: MultiModelRowCountResults):
    assertEqual(multi_model_row_count.model_C_rows == multi_model_row_count.policy_agg_df_rows, True, f"{multi_model_row_count.sys_model_C_id}: Row Count Mismatch with Expected results")

    
def test_a_b_row_count(multi_model_row_count: MultiModelRowCountResults):
    file_path = f'{os.getcwd()}/testing/tests/a_b_tests/0_4_23_record_count.json'
    record_count_0_4_23 = json.load(open(file_path))['record_count']
    record_count_current = multi_model_row_count.result_rows
    assertEqual(record_count_current > record_count_0_4_23, True, "Invalid Row Count for current version")

