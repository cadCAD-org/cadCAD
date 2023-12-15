from typing import Dict
from cadCAD_tools import easy_run
from cadCAD_tools.types import TimestepBlock, StateVariable, Parameter
from time import time
import pandas as pd


def MEASURE_TIME_SUF(p, s, h, v, p_i): return ('run_time', time())


MEASURING_BLOCK = {
    'label': 'Time Measure',
    'policies': {},
    'variables': {
        'run_time': MEASURE_TIME_SUF
    }
}


def profile_psubs(psubs: TimestepBlock, profile_substeps=True) -> TimestepBlock:
    """
    Updates a TimestepBlock so that a time measuring function is added.
    """
    new_timestep_block = []
    new_timestep_block.append(MEASURING_BLOCK)
    if profile_substeps is True:
        for psub in psubs:
            new_timestep_block.append(psub)
            new_timestep_block.append(MEASURING_BLOCK)
    else:
        pass
    return new_timestep_block


def profile_run(state_variables: Dict[str, StateVariable],
                params: Dict[str, Parameter],
                psubs: TimestepBlock,
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
