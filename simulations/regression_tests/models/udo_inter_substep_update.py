import pandas as pd
import pprint as pp
# from fn.func import curried
from datetime import timedelta

from cadCAD.utils import SilentDF #, val_switch
from cadCAD.configuration.utils import time_step, config_sim
from cadCAD.configuration.utils.userDefinedObject import udoPipe, UDO
from simulations.regression_tests.experiments import udo1_exp

DF = SilentDF(pd.read_csv('simulations/external_data/output.csv'))

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

    # Generic update function

    pass

# can be accessed after an update within the same substep and timestep
state_udo = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoA = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoB = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])

def udo_policyA(_g, step, sL, s, **kwargs):
    s['udo_policies']['udo_A'].updateX()
    return {'udo_A': udoPipe(s['udo_policies']['udo_A'])}

def udo_policyB(_g, step, sL, s, **kwargs):
    s['udo_policies']['udo_B'].updateX()
    return {'udo_B': udoPipe(s['udo_policies']['udo_B'])}


policies = {"p1": udo_policyA, "p2": udo_policyB}

state_dict = {
    'increment': 0,
    'state_udo': state_udo, 'state_udo_tracker_a': 0, 'state_udo_tracker_b': 0,
    'state_udo_perception_tracker': {"ds1": None, "ds2": None, "ds3": None, "timestep": None},
    'udo_policies': {'udo_A': policy_udoA, 'udo_B': policy_udoB},
    'udo_policy_tracker_a': (0, 0), 'udo_policy_tracker_b': (0, 0),
    'timestamp': '2019-01-01 00:00:00'
}

# @curried
def perceive(s, self):
    self.perception = self.ds[
        (self.ds['run'] == s['run']) & (self.ds['substep'] == s['substep']) & (self.ds['timestep'] == s['timestep'])
    ].drop(columns=['run', 'substep']).to_dict()
    return self

def view_udo_policy(_g, step, sL, s, _input, **kwargs):
    return 'udo_policies', _input

def state_udo_update(_g, step, sL, s, _input, **kwargs):
    y = 'state_udo'
    # s['hydra_state'].updateX().anon(perceive(s))
    s['state_udo'].updateX().perceive(s)
    x = udoPipe(s['state_udo'])
    return y, x

def increment(y, incr_by):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y] + incr_by)

def track(destination, source):
    return lambda _g, step, sL, s, _input, **kwargs: (destination, s[source].x)

def track_udo_policy(destination, source):
    def val_switch(v):
        if isinstance(v, pd.DataFrame) is True or isinstance(v, SilentDF) is True:
            return SilentDF(v)
        else:
            return v.x
    return lambda _g, step, sL, s, _input, **kwargs: (destination, tuple(val_switch(v) for _, v in s[source].items()))

def track_state_udo_perception(destination, source):
    def id(past_perception):
        if len(past_perception) == 0:
            return state_dict['state_udo_perception_tracker']
        else:
            return past_perception
    return lambda _g, step, sL, s, _input, **kwargs: (destination, id(s[source].perception))


def time_model(y, substeps, time_delta, ts_format='%Y-%m-%d %H:%M:%S'):
    def apply_incriment_condition(s):
        if s['substep'] == 0 or s['substep'] == substeps:
            return y, time_step(dt_str=s[y], dt_format=ts_format, _timedelta=time_delta)
        else:
            return y, s[y]
    return lambda _g, step, sL, s, _input, **kwargs: apply_incriment_condition(s)


states = {
    'increment': increment('increment', 1),
    'state_udo_tracker_a': track('state_udo_tracker_a', 'state_udo'),
    'state_udo': state_udo_update,
    'state_udo_perception_tracker': track_state_udo_perception('state_udo_perception_tracker', 'state_udo'),
    'state_udo_tracker_b': track('state_udo_tracker_b', 'state_udo'),
    'udo_policy_tracker_a': track_udo_policy('udo_policy_tracker_a', 'udo_policies'),
    'udo_policies': view_udo_policy,
    'udo_policy_tracker_b': track_udo_policy('udo_policy_tracker_b', 'udo_policies')
}

substeps=3
update_timestamp = time_model(
    'timestamp',
    substeps=3,
    time_delta=timedelta(days=0, minutes=0, seconds=1),
    ts_format='%Y-%m-%d %H:%M:%S'
)
states['timestamp'] = update_timestamp

PSUB = {
    'policies': policies,
    'states': states
}

# needs M1&2 need behaviors
partial_state_update_blocks = [PSUB] * substeps
# pp.pprint(partial_state_update_blocks)

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

udo1_exp.append_configs(
    sim_configs=sim_config,
    initial_state=state_dict,
    seeds={},
    raw_exogenous_states={},
    env_processes={},
    partial_state_update_blocks=partial_state_update_blocks,
    # policy_ops=[lambda a, b: {**a, **b}]
)

print()
print("State Updates:")
pp.pprint(partial_state_update_blocks)
print()