from datetime import timedelta

from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim
from cadCAD.configuration.utils.policyAggregation import dict_op, dict_elemwise_sum
from cadCAD.configuration.utils.udo import udcBroker, udoPipe, UDO


# ToDo: Create member for past value
class MyClass(object):
    def __init__(self, x):
        self.x = x

    def update(self):
        self.x += 1
        return self

    def getMemID(self):
        return str(hex(id(self)))

    pass


# can be accessed after an update within the same substep and timestep

hydra_state_view = UDO(MyClass(0))
udc_view_B = UDO(MyClass(0))
udc_view_C = UDO(MyClass(0))

# g: Dict[str, List[int]] = {'MyClassB'}

state_dict = {
    'a': 0, 'b': 0, 'j': 0,
    'k': (0, 0), 'q': (0, 0),
    'hydra_state': hydra_state_view,
    'policies': {'hydra_B': udc_view_B, 'hydra_C': udc_view_C},
    'timestamp': '2019-01-01 00:00:00'
}

def p1(_g, step, sL, s):
    s['policies']['hydra_B'].update()
    return {'hydra_B': udoPipe(s['policies']['hydra_B'])}

def p2(_g, step, sL, s):
    s['policies']['hydra_C'].update()
    return {'hydra_C': udoPipe(s['policies']['hydra_C'])}

def policies(_g, step, sL, s, _input):
    y = 'policies'
    x = _input
    return (y, x)

timestep_duration = timedelta(minutes=1) # In this example, a timestep has a duration of 1 minute.
ts_format = '%Y-%m-%d %H:%M:%S'
def time_model(_g, step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=timestep_duration)
    return (y, x)


def HydraMembers(_g, step, sL, s, _input):
    y = 'hydra_state'
    s['hydra_state'].update()
    x = udoPipe(s['hydra_state'])
    return (y, x)

def repr(_g, step, sL, s, _input):
    y = 'z'
    x = s['hydra_members'].__repr__()
    return (y, x)

def incriment(y, incr_val):
    return lambda _g, step, sL, s, _input: (y, s[y] + incr_val)

def A(_g, step, sL, s, _input):
    y = 'a'
    x = s['a'] + 1
    return (y, x)

def hydra_state_tracker(y):
    return lambda _g, step, sL, s, _input: (y, s['hydra_state'].x)


def hydra_policy_tracker(y):
    return lambda _g, step, sL, s, _input: (y, tuple(v.x for k, v in s['policies'].items()))


# needs M1&2 need behaviors
partial_state_update_blocks = {
    'PSUB1': {
        'policies': {
            "b1": p1,
            "b2": p2
        },
        'states': {
            'a': A,
            'b': hydra_state_tracker('b'),
            'j': hydra_state_tracker('j'),
            'k': hydra_policy_tracker('k'),
            'q': hydra_policy_tracker('q'),
            'hydra_state': HydraMembers,
            'timestamp': time_model,
            'policies': policies
        }
    },
    'PSUB2': {
        'policies': {
            "b1": p1,
            "b2": p2
        },
        'states': {
            'a': A,
            'b': hydra_state_tracker('b'),
            'j': hydra_state_tracker('j'),
            'k': hydra_policy_tracker('k'),
            'q': hydra_policy_tracker('q'),
            'hydra_state': HydraMembers,
            'policies': policies
        }
    },
    'PSUB3': {
        'policies': {
            "b1": p1,
            "b2": p2
        },
        'states': {
            'a': A,
            'b': hydra_state_tracker('b'),
            'j': hydra_state_tracker('j'),
            'k': hydra_policy_tracker('k'),
            'q': hydra_policy_tracker('q'),
            'hydra_state': HydraMembers,
            'policies': policies
        }
    }
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

append = lambda a, b: [a, b]
update_dict = lambda a, b: a.update(b)
take_first = lambda a, b: [a, b]
append_configs(sim_config, state_dict, {}, {}, {}, partial_state_update_blocks)#, policy_ops=[foldr(dict_op(take_first))])
