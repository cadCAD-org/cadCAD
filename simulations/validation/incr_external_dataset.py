from datetime import timedelta

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim
# from cadCAD.configuration.utils.policyAggregation import dict_op, dict_elemwise_sum
from cadCAD.configuration.utils.userDefinedObject import udcBroker, udoPipe, UDO
import pandas as pd
from cadCAD.utils import SilentDF

df = SilentDF(pd.read_csv('/Users/jjodesty/Projects/DiffyQ-SimCAD/simulations/output.csv'))

state_dict = {
    'increment': 0,
    'external_data': {"ds1": None, "ds2": None, "ds3": None},
    'policies': {}
}

def query(s, df):
    return df[
            (df['run'] == s['run']) & (df['substep'] == s['substep']) & (df['timestep'] == s['timestep'])
        ].drop(columns=['run', 'substep', "timestep"])

def p1(_g, substep, sL, s):
    result_dict = query(s, df).to_dict()
    del result_dict["ds3"]
    return {k: list(v.values()).pop() for k, v in result_dict.items()}

def p2(_g, step, sL, s):
    result_dict = query(s, df).to_dict()
    del result_dict["ds1"], result_dict["ds2"]
    return {k: list(v.values()).pop() for k, v in result_dict.items()}

# ToDo: SilentDF(df) wont work
#integrate_ext_dataset
def integrate_ext_dataset(_g, step, sL, s, _input):
    result_dict = query(s, df).to_dict()
    return 'external_data', {k: list(v.values()).pop() for k, v in result_dict.items()}

def increment(y, incr_by):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)
increment = increment('increment', 1)

def view_policies(_g, step, sL, s, _input):
    return 'policies', _input


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

append_configs(
    sim_config,
    state_dict,
    {}, {}, {},
    partial_state_update_blocks,
    policy_ops=[lambda a, b: {**a, **b}]
)
