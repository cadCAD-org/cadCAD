from datetime import timedelta
from cadCAD.utils import SilentDF #, val_switch
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim
from cadCAD.configuration.utils.userDefinedObject import udoPipe, UDO
import pandas as pd

from fn.func import curried

DF = SilentDF(pd.read_csv('/Users/jjodesty/Projects/DiffyQ-SimCAD/simulations/output.csv'))

class udoExample(object):
    def __init__(self, x, dataset=None):
        self.x = x
        self.mem_id = str(hex(id(self)))
        self.ds = dataset # for setting ds initially or querying
        self.perception = {}

    def anon(self, f):
        return f(self)

    def updateX(self):
        self.x += 1
        return self

    def perceive(self, s):
        self.perception = self.ds[
            (self.ds['run'] == s['run']) & (self.ds['substep'] == s['substep']) & (self.ds['timestep'] == s['timestep'])
        ].drop(columns=['run', 'substep']).to_dict()
        return self

    def read(self, ds_uri):
        self.ds = SilentDF(pd.read_csv(ds_uri))
        return self

    def write(self, ds_uri):
        pd.to_csv(ds_uri)

    # ToDo: Generic update function

    pass

# can be accessed after an update within the same substep and timestep

state_udo = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoA = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoB = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])

# ToDo: DataFrame Column order
state_dict = {
    'increment': 0,
    'state_udo': state_udo, 'state_udo_tracker_a': 0, 'state_udo_tracker_b': 0,
    'state_udo_perception_tracker': {"ds1": None, "ds2": None, "ds3": None, "timestep": None},
    'udo_policies': {'udo_A': policy_udoA, 'udo_B': policy_udoB},
    'udo_policy_tracker_a': (None, None), 'udo_policy_tracker_b': (None, None),
    'timestamp': '2019-01-01 00:00:00',
}

@curried
def perceive(s, self):
    self.perception = self.ds[
        (self.ds['run'] == s['run']) & (self.ds['substep'] == s['substep']) & (self.ds['timestep'] == s['timestep'])
    ].drop(columns=['run', 'substep']).to_dict()
    return self

def view_udo_policy(_g, step, sL, s, _input):
    y = 'udo_policies'
    x = _input
    return (y, x)

def update_timestamp(y, timedelta, format):
    return lambda _g, step, sL, s, _input: (
        y,
        ep_time_step(s, dt_str=s[y], fromat_str=format, _timedelta=timedelta)
    )
time_model = update_timestamp('timestamp', timedelta(minutes=1), '%Y-%m-%d %H:%M:%S')


def state_udo_update(_g, step, sL, s, _input):
    y = 'state_udo'
    # s['hydra_state'].updateX().anon(perceive(s))
    s['state_udo'].updateX().perceive(s)
    x = udoPipe(s['state_udo'])
    return (y, x)

def increment(y, incr_by):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)

def track(destination, source):
    return lambda _g, step, sL, s, _input: (destination, s[source].x)

def track_udo_policy(destination, source):
    def val_switch(v):
        if isinstance(v, pd.DataFrame) is True or isinstance(v, SilentDF) is True:
            return SilentDF(v)
        else:
            return v.x
    return lambda _g, step, sL, s, _input: (destination, tuple(val_switch(v) for _, v in s[source].items()))

def track_state_udo_perception(destination, source):
    def id(past_perception):
        if len(past_perception) == 0:
            return state_dict['state_udo_perception_tracker']
        else:
            return past_perception
    return lambda _g, step, sL, s, _input: (destination, id(s[source].perception))

def udo_policyA(_g, step, sL, s):
    s['udo_policies']['udo_A'].updateX()
    return {'udo_A': udoPipe(s['udo_policies']['udo_A'])}

def udo_policyB(_g, step, sL, s):
    s['udo_policies']['udo_B'].updateX()
    return {'udo_B': udoPipe(s['udo_policies']['udo_B'])}

policies = {"p1": udo_policyA, "p2": udo_policyB}

states_with_ts = {
    'increment': increment('increment', 1),
    'state_udo_tracker_a': track('state_udo_tracker_a', 'state_udo'),
    'state_udo': state_udo_update,
    'state_udo_perception_tracker': track_state_udo_perception('state_udo_perception_tracker', 'state_udo'),
    'state_udo_tracker_b': track('state_udo_tracker_b', 'state_udo'),
    'udo_policy_tracker_a': track_udo_policy('udo_policy_tracker_a', 'udo_policies'),
    'udo_policies': view_udo_policy,
    'udo_policy_tracker_b': track_udo_policy('udo_policy_tracker_b', 'udo_policies'),
    'timestamp': time_model,
}
del states_with_ts['timestamp']
states_without_ts = states_with_ts

# needs M1&2 need behaviors
partial_state_update_blocks = {
    'PSUB1': {
        'policies': policies,
        'states': states_with_ts
    },
    'PSUB2': {
        'policies': policies,
        'states': states_without_ts
    },
    'PSUB3': {
        'policies': policies,
        'states': states_without_ts
    }
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
