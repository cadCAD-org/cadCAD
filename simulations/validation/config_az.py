from copy import deepcopy
from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step
from cadCAD.configuration.utils.parameterSweep import config_sim


class MyClass:
    def __init__(self):
        self.x = 0
        print(f"Instance of MyClass (mem_id {hex(id(self))}) created with value {self.x}")

    def update(self):
        # res = deepcopy(self)
        self.x += 1
        # print(f"Instance of MyClass (mem_id {hex(id(self))}) has been updated, has now value {self.x}")
        return self #res

    def __str__(self):
        return f"PRINT MyClass: @ {hex(id(self))}: value {self.x}"

# genesis state
state_dict = {
    'classX': MyClass(),
    'a': 0,
    'b': 0,
    'timestamp': '2019-01-01 00:00:00'
}


timestep_duration = timedelta(minutes=1) # In this example, a timestep has a duration of 1 minute.
ts_format = '%Y-%m-%d %H:%M:%S'
def time_model(_g, step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=timestep_duration)
    return (y, x)


def updateClassX(_g, step, sL, s, _input):
    y = 'classX'
    x = s['classX']
    return (y, x)


def updateA(_g, step, sL, s, _input):
    y = 'a'
    x = s['a'] + 1
    return (y, x)


def updateB(_g, step, sL, s, _input):
    s['classX'].update()
    y = 'b'
    x = s['classX'].x
    return (y, x)


partial_state_update_blocks = {
    'PSUB1': { 
        'behaviors': { 
        },
        'states': { 
            'timestamp': time_model
        }
    },
    'PSUB2': { 
        'behaviors': { 
        },
        'states': {
            'classX': updateClassX,
            'a': updateA,
            'b': updateB
        }
    },
    'PSUB3': { 
        'behaviors': { 
        },
        'states': { 
            'classX': updateClassX,
            'a': updateA,
            'b': updateB
        }
    }
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

append_configs(sim_config, state_dict, {}, {}, {}, partial_state_update_blocks)
