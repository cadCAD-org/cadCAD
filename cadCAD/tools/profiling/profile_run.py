from typing import Dict
from cadCAD.tools import easy_run
from cadCAD.types import StateUpdateBlocks, Parameters, State, StateUpdateBlock
from time import time
import pandas as pd # type: ignore


def MEASURE_TIME_SUF(p, s, h, v, p_i): return ('run_time', time())


MEASURING_BLOCK: StateUpdateBlock = {
    'label': 'Time Measure',
    'policies': {},
    'variables': {
        'run_time': MEASURE_TIME_SUF
    }
} # type: ignore


def profile_psubs(psubs: StateUpdateBlocks, profile_substeps=True) -> StateUpdateBlocks:
    """
    Updates a TimestepBlock so that a time measuring function is added.
    """
    new_timestep_block: StateUpdateBlocks = []
    new_timestep_block.append(MEASURING_BLOCK)
    if profile_substeps is True:
        for psub in psubs:
            new_timestep_block.append(psub)
            new_timestep_block.append(MEASURING_BLOCK)
    else:
        pass
    return new_timestep_block


def profile_run(state_variables: State,
                params: Parameters,
                psubs: StateUpdateBlocks,
                *args,
                profile_substeps=True,
                **kwargs) -> pd.DataFrame:

    if profile_substeps is True:
        kwargs.update(drop_substeps=False)

    new_psubs = profile_psubs(psubs, profile_substeps)
    state_variables.update({'run_time': None})

    return easy_run(state_variables,
                    params,
                    new_psubs,
                    *args,
                    **kwargs)
