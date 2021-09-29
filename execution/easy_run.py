from typing import Dict, Union
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import config_sim
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
import pandas as pd


def select_M_dict(M_dict: Dict[str, object], keys: set) -> Dict[str, object]:
    return {k: v for k, v in M_dict.items()
            if k in keys}


def select_config_M_dict(configs: list, i: int, keys: set) -> Dict[str, object]:
    return select_M_dict(configs[i].sim_config['M'], keys)


def easy_run(state_variables,
             params,
             psubs,
             N_timesteps,
             N_samples,
             use_label=False,
             assign_params: Union[bool, set]=True,
             drop_substeps=True) -> pd.DataFrame:
    """
    Run cadCAD simulations without headaches.
    """

    # Set-up sim_config
    simulation_parameters = {
        'N': N_samples,
        'T': range(N_timesteps),
        'M': params
    }
    sim_config = config_sim(simulation_parameters)

    # Create a new experiment
    exp = Experiment()
    exp.append_configs(sim_configs=sim_config,
                       initial_state=state_variables,
                       partial_state_update_blocks=psubs)
    configs = exp.configs
    
    # Set-up cadCAD executor
    exec_mode = ExecutionMode()
    exec_context = ExecutionContext(exec_mode.local_mode)
    executor = Executor(exec_context=exec_context, configs=configs)

    # Execute the cadCAD experiment
    (records, tensor_field, _) = executor.execute()

    # Parse the output as a pandas DataFrame
    df = pd.DataFrame(records)

    if drop_substeps == True:
        # Drop all intermediate substeps
        first_ind = (df.substep == 0) & (df.timestep == 0)
        last_ind = df.substep == max(df.substep)
        inds_to_drop = (first_ind | last_ind)
        df = df.loc[inds_to_drop].drop(columns=['substep'])
    else:
        pass

    if assign_params == False:
        pass
    else:
        M_dict = configs[0].sim_config['M']
        params_set = set(M_dict.keys())
        
        if assign_params == True:
            pass
        else:
            params_set &= assign_params

        # Logic for getting the assign params criteria
        if type(assign_params) is list:
            selected_params = set(assign_params) & params_set
        elif type(assign_params) is set:
            selected_params = assign_params & params_set
        else:
            selected_params = params_set

        # Attribute parameters to each row
        df = df.assign(**select_config_M_dict(configs, 0, selected_params))
        for i, (_, n_df) in enumerate(df.groupby(['simulation', 'subset', 'run'])):
            df.loc[n_df.index] = n_df.assign(**select_config_M_dict(configs,
                                                                    i,
                                                                    selected_params))

    # Based on Vitor Marthendal (@marthendalnunes) snippet
    if use_label == True:
        psub_map = {order + 1: psub.get('label', '')
                    for (order, psub)
                    in enumerate(psubs)}
        psub_map[0] = 'Initial State'
        df['substep_label'] = df.substep.map(psub_map)

    return df
