from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim
from copy import deepcopy


# ToDo: Create member for past value
class MyClass:
    def __init__(self, past_attr):
        self.past_self = self
        self.past_attr = past_attr
        self.class_id = None
        self.x = 0

        print(f"Instance of MyClass (mem_id {hex(id(self))}) created with value {self.x}")

    def update(self):
        # self.past_self = deepcopy(self)
        self.x += 1
        print(f"Instance of MyClass (mem_id {hex(id(self))}) has been updated, has now value {self.x}")
        return self.x #self #old_self #self.x

    def past(self):
        return self.past_self

    def getMemID(self):
        return str(hex(id(self)))

    # can be accessed after an update within the same substep and timestep
    # ToDo: id sensitive to lineage, rerepresent
    def __str__(self):
        # return str(self.x)
        return f"{hex(id(self))} - {self.x}"


# a is Correct, and classX's value is Incorrect
# Expected: a == classX's value
# b should be tracking classX's value and a:
#     b should be the same value as the previous classX value and the previous a value

udc = MyClass('pastX')

# z = MyClass()
# pointer(z)
# separate thread/process for UCD with async calls to this thread/process

# genesis state

# udc_json = {'udc': udc, 'udc-1': udc}
state_dict = {
    'classX': udc,
    'classX_MemID': udc.getMemID(),
    # 'pastX': udc,
    # 'pastX_MemID': udc.getMemID(),
    'a': 0,
    'b': udc.x,
    'c': udc.x,
    'c2': udc.x,
    'z': udc.x,
    'timestamp': '2019-01-01 00:00:00'
}

timestep_duration = timedelta(minutes=1) # In this example, a timestep has a duration of 1 minute.
ts_format = '%Y-%m-%d %H:%M:%S'
def time_model(_g, step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=timestep_duration)
    return (y, x)

def trackClassX(_g, step, sL, s, _input):
    y = 'classX'
    x = s['classX']
    return (y, x)

def trackClassX_str(_g, step, sL, s, _input):
    y = 'classX_MemID'
    x = s['classX'].getMemID()
    return (y, x)

def updatePastX(_g, step, sL, s, _input):
    y = 'pastX'
    x = s['pastX']
    return (y, x)

def updatePastX_str(_g, step, sL, s, _input):
    y = 'pastX_MemID'
    x = s['pastX'].getMemID()
    return (y, x)

def updateA(_g, step, sL, s, _input):
    y = 'a'
    x = s['a'] + 1
    return (y, x)

def updateB(_g, step, sL, s, _input):
    y = 'b'
    x = s['classX'].x
    return (y, x)

def updateC(_g, step, sL, s, _input):
    y = 'c'
    x = s['classX'].update()
    return (y, x)

def updateZ(_g, step, sL, s, _input):
    y = 'z'
    x = s['classX'].x
    return (y, x)

def updateC2(_g, step, sL, s, _input):
    y = 'c2'
    x = s['classX'].x
    return (y, x)

partial_state_update_blocks = {
    'PSUB1': {
        'behaviors': {
        },
        'states': {
            'a': updateA,
            'b': updateB,
            'c': updateC,
            'c2': updateC2,
            'classX': trackClassX,
            'timestamp': time_model,
            'classX_MemID': trackClassX_str,
            # 'pastX': updatePastX,
            # 'pastX_MemID': updatePastX_str,
            'z': updateZ
        }
    },
    'PSUB2': {
        'behaviors': {
        },
        'states': {
            'a': updateA,
            'b': updateB,
            'c': updateC,
            'c2': updateC2,
            'classX': trackClassX,
            'classX_MemID': trackClassX_str,
            # 'pastX': updatePastX,
            # 'pastX_MemID': updatePastX_str,
            'z': updateZ
        }
    },
    'PSUB3': {
        'behaviors': {
        },
        'states': {
            'a': updateA,
            'b': updateB,
            'c': updateC,
            'c2': updateC2,
            'classX': trackClassX,
            'classX_MemID': trackClassX_str,
            # 'pastX': updatePastX,
            # 'pastX_MemID': updatePastX_str,
            'z': updateZ
        }
    }
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

append_configs(sim_config, state_dict, {}, {}, {}, partial_state_update_blocks)
