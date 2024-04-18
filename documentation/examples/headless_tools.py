# isort:skip_file
# fmt: off
import sys
sys.path.append(".")
from cadCAD.tools import easy_run
import plotly.express as px
import numpy as np
import sys
import seaborn as sns
from tqdm.auto import tqdm
# fmt: on 


TIMESTEPS = 3650
SAMPLES = 2
GARBAGE_SIZE = 100000
# STATE_SIZE = 1
STATE_SIZE = 100000

initial_conditions = {
    'big_state':  "a" * STATE_SIZE
}

params = {
    'big_param':  ["p" * GARBAGE_SIZE]
}


def p_big_policy(params, step, sL, s):
    y = 'big_state'
    x = s['big_state'] + "a"
    return {'big_state': x}


def s_big_state(params, step, sL, s, _input):
    y = 'big_state'
    x = s['big_state'] + "b"
    return (y, x)


partial_state_update_blocks = [
    {
        'label': 'Memory Consumer',
        'policies': {
            'big_policy': p_big_policy,
        },
        'variables': {
            'big_state': s_big_state
        }
    },
    {
        'label': 'Do Nothing',
        'policies': {

        },
        'variables': {

        }
    }
]


df = easy_run(initial_conditions,
              params,
              partial_state_update_blocks,
              TIMESTEPS,
              SAMPLES,
              deepcopy_off=True,
              lazy_eval=True,
              assign_params=True,
              drop_substeps=False)
print(df)
