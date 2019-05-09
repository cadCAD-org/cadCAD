from copy import deepcopy
from datetime import timedelta
from functools import reduce

from cadCAD.utils import SilentDF #, val_switch
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import time_step, config_sim, proc_trigger, timestep_trigger, genereate_psubs
from cadCAD.configuration.utils.userDefinedObject import udoPipe, UDO
import pandas as pd

from fn.func import curried

import pprint as pp

from cadCAD.utils.sys_config import add

DF = SilentDF(pd.read_csv('/Users/jjodesty/Projects/DiffyQ-SimCAD/simulations/external_data/output.csv'))


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


state_udo = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoA = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])
policy_udoB = UDO(udo=udoExample(0, DF), masked_members=['obj', 'perception'])


sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

# ToDo: DataFrame Column order
state_dict = {
    'increment': 0,
    'state_udo': state_udo, 'state_udo_tracker': 0,
    'state_udo_perception_tracker': {"ds1": None, "ds2": None, "ds3": None, "timestep": None},
    'udo_policies': {'udo_A': policy_udoA, 'udo_B': policy_udoB},
    'udo_policy_tracker': (0, 0),
    'timestamp': '2019-01-01 00:00:00'
}

policies, state_updates = {}, {}
#
# def assign_udo_policy(udo):
#     def policy(_g, step, sL, s):
#         s['udo_policies'][udo].updateX()
#         return {udo: udoPipe(s['udo_policies'][udo])}
#     return policy
# policies_updates = {p: assign_udo_policy(udo) for p, udo in zip(['p1', 'p2'], ['udo_A', 'udo_B'])}

def udo_policyA(_g, step, sL, s):
    s['udo_policies']['udo_A'].updateX()
    return {'udo_A': udoPipe(s['udo_policies']['udo_A'])}
policies['a'] = udo_policyA

def udo_policyB(_g, step, sL, s):
    s['udo_policies']['udo_B'].updateX()
    return {'udo_B': udoPipe(s['udo_policies']['udo_B'])}
policies['b'] = udo_policyB


# policies = {"p1": udo_policyA, "p2": udo_policyB}
# policies = {"A": udo_policyA, "B": udo_policyB}

# def increment_state_by_int(y: str, incr_by: int):
#     return lambda _g, step, sL, s, _input: (y, s[y] + incr_by)
state_updates['increment'] = add('increment', 1)

@curried
def perceive(s, self):
    self.perception = self.ds[
        (self.ds['run'] == s['run']) & (self.ds['substep'] == s['substep']) & (self.ds['timestep'] == s['timestep'])
    ].drop(columns=['run', 'substep']).to_dict()
    return self


def state_udo_update(_g, step, sL, s, _input):
    y = 'state_udo'
    # s['hydra_state'].updateX().anon(perceive(s))
    s['state_udo'].updateX().perceive(s)
    x = udoPipe(s['state_udo'])
    return y, x
state_updates['state_udo'] = state_udo_update


def track(destination, source):
    return lambda _g, step, sL, s, _input: (destination, s[source].x)
state_updates['state_udo_tracker'] = track('state_udo_tracker', 'state_udo')


def track_state_udo_perception(destination, source):
    def id(past_perception):
        if len(past_perception) == 0:
            return state_dict['state_udo_perception_tracker']
        else:
            return past_perception
    return lambda _g, step, sL, s, _input: (destination, id(s[source].perception))
state_updates['state_udo_perception_tracker'] = track_state_udo_perception('state_udo_perception_tracker', 'state_udo')


def view_udo_policy(_g, step, sL, s, _input):
    return 'udo_policies', _input
state_updates['udo_policies'] = view_udo_policy


def track_udo_policy(destination, source):
    def val_switch(v):
        if isinstance(v, pd.DataFrame) is True or isinstance(v, SilentDF) is True:
            return SilentDF(v)
        else:
            return v.x
    return lambda _g, step, sL, s, _input: (destination, tuple(val_switch(v) for _, v in s[source].items()))
state_updates['udo_policy_tracker'] = track_udo_policy('udo_policy_tracker', 'udo_policies')

def update_timestamp(_g, step, sL, s, _input):
    y = 'timestamp'
    return y, time_step(dt_str=s[y], dt_format='%Y-%m-%d %H:%M:%S', _timedelta=timedelta(days=0, minutes=0, seconds=1))


system_substeps = 3
# state_updates['timestamp'] = update_timestamp
state_updates['timestamp'] = timestep_trigger(end_substep=system_substeps, y='timestamp', f=update_timestamp)
# state_updates['timestamp'] = proc_trigger(y='timestamp', f=update_timestamp, conditions={'substep': [0, substeps]}, cond_op=lambda a, b: a and b)

print()
print("State Updates:")
pp.pprint(state_updates)
print()
print("Policies:")
pp.pprint(policies)
print()

filter_out = lambda remove_list, state_list: list(filter(lambda state: state not in remove_list, state_list))

states = list(state_updates.keys())
# states_noTS = filter_out(['timestamp'], states)
# states_grid = [states,states_noTS,states_noTS]

# states_grid = [states] * system_substeps #
states_grid = [states,states,states]
policy_grid = [['a', 'b'], ['a', 'b'], ['a', 'b']]


PSUBS = genereate_psubs(policy_grid, states_grid, policies, state_updates)
pp.pprint(PSUBS)
# ToDo: Bug without specifying parameters
append_configs(
    sim_configs=sim_config,
    initial_state=state_dict,
    seeds={},
    raw_exogenous_states={},
    env_processes={},
    partial_state_update_blocks=PSUBS,
    # policy_ops=[lambda a, b: {**a, **b}]
)

# pp.pprint(partial_state_update_blocks)

# PSUB = {
#     'policies': policies,
#     'states': state_updates
# }
# partial_state_update_blocks = [PSUB] * substeps


