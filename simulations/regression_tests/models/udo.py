import pandas as pd
from datetime import timedelta
import pprint as pp

from cadCAD.utils import SilentDF
from cadCAD.configuration.utils import time_step, config_sim, var_trigger, var_substep_trigger, env_trigger, psub_list
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

    def updateDS(self):
        self.ds.iloc[0,0] -= 10
        # pp.pprint(self.ds)
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

    pass


state_udo = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoA = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoB = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])


sim_config = config_sim({
    "N": 3,
    "T": range(4)
})

state_dict = {
    'increment': 0,
    'state_udo': state_udo, 'state_udo_tracker': 0,
    'state_udo_perception_tracker': {"ds1": None, "ds2": None, "ds3": None, "timestep": None},
    'udo_policies': {'udo_A': policy_udoA, 'udo_B': policy_udoB},
    'udo_policy_tracker': (0, 0),
    'timestamp': '2019-01-01 00:00:00'
}

psu_steps = ['m1', 'm2', 'm3']
system_substeps = len(psu_steps)
var_timestep_trigger = var_substep_trigger([0, system_substeps])
env_timestep_trigger = env_trigger(system_substeps)
psu_block = {k: {"policies": {}, "variables": {}} for k in psu_steps}

def udo_policyA(_g, step, sL, s, **kwargs):
    s['udo_policies']['udo_A'].updateX()
    return {'udo_A': udoPipe(s['udo_policies']['udo_A'])}
# policies['a'] = udo_policyA
for m in psu_steps:
    psu_block[m]['policies']['a'] = udo_policyA

def udo_policyB(_g, step, sL, s, **kwargs):
    s['udo_policies']['udo_B'].updateX()
    return {'udo_B': udoPipe(s['udo_policies']['udo_B'])}
# policies['b'] = udo_policyB
for m in psu_steps:
    psu_block[m]['policies']['b'] = udo_policyB


# policies = {"p1": udo_policyA, "p2": udo_policyB}
# policies = {"A": udo_policyA, "B": udo_policyB}

def add(y: str, added_val):
    return lambda _g, step, sL, s, _input, **kwargs: (y, s[y] + added_val)
# state_updates['increment'] = add('increment', 1)
for m in psu_steps:
    psu_block[m]["variables"]['increment'] = add('increment', 1)


# @curried
def perceive(s, self):
    self.perception = self.ds[
        (self.ds['run'] == s['run']) & (self.ds['substep'] == s['substep']) & (self.ds['timestep'] == s['timestep'])
    ].drop(columns=['run', 'substep']).to_dict()
    return self


def state_udo_update(_g, step, sL, s, _input, **kwargs):
    y = 'state_udo'
    # s['hydra_state'].updateX().anon(perceive(s))
    s['state_udo'].updateX().perceive(s).updateDS()
    x = udoPipe(s['state_udo'])
    return y, x
for m in psu_steps:
    psu_block[m]["variables"]['state_udo'] = state_udo_update


def track(destination, source):
    return lambda _g, step, sL, s, _input, **kwargs: (destination, s[source].x)
state_udo_tracker = track('state_udo_tracker', 'state_udo')
for m in psu_steps:
    psu_block[m]["variables"]['state_udo_tracker'] = state_udo_tracker


def track_state_udo_perception(destination, source):
    def id(past_perception):
        if len(past_perception) == 0:
            return state_dict['state_udo_perception_tracker']
        else:
            return past_perception
    return lambda _g, step, sL, s, _input, **kwargs: (destination, id(s[source].perception))
state_udo_perception_tracker = track_state_udo_perception('state_udo_perception_tracker', 'state_udo')
for m in psu_steps:
    psu_block[m]["variables"]['state_udo_perception_tracker'] = state_udo_perception_tracker


def view_udo_policy(_g, step, sL, s, _input, **kwargs):
    return 'udo_policies', _input
for m in psu_steps:
    psu_block[m]["variables"]['udo_policies'] = view_udo_policy


def track_udo_policy(destination, source):
    def val_switch(v):
        if isinstance(v, pd.DataFrame) is True or isinstance(v, SilentDF) is True:
            return SilentDF(v)
        else:
            return v.x
    return lambda _g, step, sL, s, _input, **kwargs: (destination, tuple(val_switch(v) for _, v in s[source].items()))
udo_policy_tracker = track_udo_policy('udo_policy_tracker', 'udo_policies')
for m in psu_steps:
    psu_block[m]["variables"]['udo_policy_tracker'] = udo_policy_tracker


def update_timestamp(_g, step, sL, s, _input, **kwargs):
    y = 'timestamp'
    return y, time_step(dt_str=s[y], dt_format='%Y-%m-%d %H:%M:%S', _timedelta=timedelta(days=0, minutes=0, seconds=1))
for m in psu_steps:
    psu_block[m]["variables"]['timestamp'] = var_timestep_trigger(y='timestamp', f=update_timestamp)
    # psu_block[m]["variables"]['timestamp'] = var_trigger(
    #     y='timestamp', f=update_timestamp,
    #     pre_conditions={'substep': [0, system_substeps]}, cond_op=lambda a, b: a and b
    # )
    # psu_block[m]["variables"]['timestamp'] = update_timestamp

# New Convention
partial_state_update_blocks = psub_list(psu_block, psu_steps)
udo1_exp.append_configs(
    sim_configs=sim_config,
    initial_state=state_dict,
    partial_state_update_blocks=partial_state_update_blocks
)

print()
print("State Updates:")
pp.pprint(partial_state_update_blocks)
print()