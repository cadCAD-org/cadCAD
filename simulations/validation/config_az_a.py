from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim


class MyClass:
    def __init__(self):
        self.x = 0
        print(f"Instance of MyClass (mem_id {hex(id(self))}) created with value {self.x}")

    def update(self):
        self.x += 1
        print(f"Instance of MyClass (mem_id {hex(id(self))}) has been updated, has now value {self.x}")
        return self

    def __str__(self):
        return f"PRINT MyClass: @ {hex(id(self))}: value {self.x}"

# a is Correct, and classX's value is Incorrect
# Expected: a == classX's value
# b should be tracking classX's value and a:
#     b should be the same value as the previous classX value and the previous a value

udc = MyClass()
# z = MyClass()
# pointer(z)
# separate thread/process for UCD with async calls to this thread/process

# genesis state
state_dict = {
    'classX': udc,
    'c_udc': udc,
    'a': 0,
    'b': 0,
    'c': "",
    'd': None,
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
    x = s['classX'].update()
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
    x = f"PRINT MyClass: @ {hex(id(s['classX']))}: value {s['classX'].x}"
    return (y, x)

def updateD(_g, step, sL, s, _input):
    y = 'd'
    x = s['classX']
    return (y, x)


partial_state_update_blocks = {
    'PSUB1': { 
        'behaviors': { 
        },
        'states': { 
            'timestamp': time_model,
            'b': updateB,
            'c': updateC,
            # 'd': updateD
        }
    },
    'PSUB2': { 
        'behaviors': { 
        },
        'states': { 
            'classX': updateClassX,
            'a': updateA,
            'b': updateB,
            'c': updateC,
            # 'd': updateD
        }
    },
    'PSUB3': { 
        'behaviors': { 
        },
        'states': { 
            'classX': updateClassX,
            'a': updateA,
            'b': updateB,
            'c': updateC,
            # 'd': updateD
        }
    }
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

append_configs(sim_config, state_dict, {}, {}, {}, partial_state_update_blocks)
