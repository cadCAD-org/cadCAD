from typing import Dict, List
from cadCAD.engine import Executor, ExecutionContext, ExecutionMode
from cadCAD.configuration import Experiment
from cadCAD.configuration.utils import env_trigger, var_substep_trigger, config_sim, psub_list
from cadCAD.types import *
import pandas as pd # type: ignore
import types
import inspect
import pytest

def test_sufs():

    psubs = [
        {
            'policies': {
                'p_A': lambda _1, _2, _3, _4: {}
            },
            'variables': {
                'v_A': lambda _1, _2, _3, _4, _5: ('a', 1)
            }
        }
    ]

    initial_state = {
        'v_A': None
    }

    params = {'p_A': [1]}

    N_t = 5
    N_r = 1

    sim_config = config_sim(
        {
            "N": N_r,
            "T": range(N_t),
            "M": params, # Optional
        }
    )

    exp = Experiment()
    exp.append_model(
        sim_configs=sim_config,
        initial_state=initial_state,
        partial_state_update_blocks=psubs
    )

    mode = ExecutionMode().local_mode
    exec_context = ExecutionContext(mode, additional_objs={'deepcopy_off': True})
    executor = Executor(exec_context=exec_context, configs=exp.configs)
    (records, tensor_field, _) = executor.execute()
