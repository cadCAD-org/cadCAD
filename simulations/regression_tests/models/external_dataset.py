from cadCAD.configuration.utils import config_sim
import pandas as pd
from cadCAD.utils import SilentDF
from simulations.regression_tests.experiments import ext_ds_exp

df = SilentDF(pd.read_csv('simulations/external_data/output.csv'))


def query(s, df):
    return df[
            (df['run'] == s['run']) & (df['substep'] == s['substep']) & (df['timestep'] == s['timestep'])
        ].drop(columns=['run', 'substep', "timestep"])

def p1(_g, substep, sL, s, **kwargs):
    result_dict = query(s, df).to_dict()
    del result_dict["ds3"]
    return {k: list(v.values()).pop() for k, v in result_dict.items()}

def p2(_g, substep, sL, s, **kwargs):
    result_dict = query(s, df).to_dict()
    del result_dict["ds1"], result_dict["ds2"]
    return {k: list(v.values()).pop() for k, v in result_dict.items()}

#integrate_ext_dataset
def integrate_ext_dataset(_g, step, sL, s, _input, **kwargs):
    result_dict = query(s, df).to_dict()
    return 'external_data', {k: list(v.values()).pop() for k, v in result_dict.items()}

def increment(y, incr_by):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y] + incr_by)
increment = increment('increment', 1)

def view_policies(_g, step, sL, s, _input, **kwargs):
    return 'policies', _input


external_data = {'ds1': None, 'ds2': None, 'ds3': None}
state_dict = {
    'increment': 0,
    'external_data': external_data,
    'policies': external_data
}


policies = {"p1": p1, "p2": p2}
states = {'increment': increment, 'external_data': integrate_ext_dataset, 'policies': view_policies}
PSUB = {'policies': policies, 'states': states}

# needs M1&2 need behaviors
partial_state_update_blocks = {
    'PSUB1': PSUB,
    'PSUB2': PSUB,
    'PSUB3': PSUB
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

ext_ds_exp.append_configs(
    sim_configs=sim_config,
    initial_state=state_dict,
    partial_state_update_blocks=partial_state_update_blocks,
    policy_ops=[lambda a, b: {**a, **b}]
)
