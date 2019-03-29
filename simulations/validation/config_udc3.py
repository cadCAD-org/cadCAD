from datetime import timedelta
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import ep_time_step, config_sim


# ToDo: Create member for past value
class MyClassA:
    def __init__(self):
        self.class_id = None
        self.x = 0

        print(f"Instance of MyClass (mem_id {hex(id(self))}) created with value {self.x}")


    def update(self):
        # self.past = copy(self)
        self.x += 1
        print(f"Instance of MyClass (mem_id {hex(id(self))}) has been updated, has now value {self.x}")
        return self.x #self #old_self #self.x


    def getMemID(self):
        return str(hex(id(self)))

    # can be accessed after an update within the same substep and timestep
    # ToDo: id sensitive to lineage, rerepresent
    def __str__(self):
        # return str(self.x)
        return f"{hex(id(self))} - {self.x}"


class MyClassB:
    def __init__(self):
        self.class_id = None
        self.x = 5

        print(f"Instance of MyClass (mem_id {hex(id(self))}) created with value {self.x}")


    def update(self):
        # self.past = copy(self)
        self.x += 1
        print(f"Instance of MyClass (mem_id {hex(id(self))}) has been updated, has now value {self.x}")
        return self.x #self #old_self #self.x


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
# https://pymotw.com/2/multiprocessing/communication.html
udcA = MyClassA()
udcB = MyClassB()

# z = MyClass()
# pointer(z)
# separate thread/process for UCD with async calls to this thread/process

# genesis state

# udc_json = {'udc': udc, 'udc-1': udc}
state_dict = {
    'ca': 0,
    'cb': udcA.x,
    'cblassX': udcA,
    'cc': udcA.x,
    'cz': udcA.x,
    'da': 5,
    'db': udcB.x,
    'dblassX': udcB,
    'dc': udcB.x,
    'dz': udcB.x,
    'timestamp': '2019-01-01 00:00:00'
}

timestep_duration = timedelta(minutes=1) # In this example, a timestep has a duration of 1 minute.
ts_format = '%Y-%m-%d %H:%M:%S'
def time_model(_g, step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, dt_str=s['timestamp'], fromat_str=ts_format, _timedelta=timestep_duration)
    return (y, x)

def CBlassX(_g, step, sL, s, _input):
    y = 'cblassX'
    # x = s['cblassX']
    x = _g['cblassX']
    return (y, x)

def DBlassX(_g, step, sL, s, _input):
    y = 'dblassX'
    # x = s['dblassX']
    x = _g['dblassX']
    return (y, x)


def CA(_g, step, sL, s, _input):
    y = 'ca'
    x = s['ca'] + 1
    return (y, x)

def DA(_g, step, sL, s, _input):
    y = 'da'
    x = s['da'] + 1
    return (y, x)

def CB(_g, step, sL, s, _input):
    y = 'cb'
    x = _g['cblassX'].x
    # x = s['cblassX'].x
    return (y, x)

def DB(_g, step, sL, s, _input):
    y = 'db'
    x = _g['dblassX'].x
    # x = s['dblassX'].x
    return (y, x)

def CC(_g, step, sL, s, _input):
    y = 'cc'
    # x = s['cblassX'].update()
    x = _g['cblassX'].update()
    return (y, x)

def DC(_g, step, sL, s, _input):
    # s['dblassX'] = _g['dblassX'].update()

    y = 'dc'
    # x = s['dblassX'].update()
    x = _g['dblassX'].update()
    return (y, x)

def CZ(_g, step, sL, s, _input):
    y = 'cz'
    x = _g['cblassX'].x
    # x = s['cblassX'].x
    return (y, x)

def DZ(_g, step, sL, s, _input):
    y = 'dz'
    x = _g['dblassX'].x
    # x = s['dblassX'].x
    return (y, x)

partial_state_update_blocks = {
    'PSUB1': {
        'behaviors': {
        },
        'states': {
            'ca': CA,
            'cb': CB,
            'cblassX': CBlassX,
            'cc': CC,
            'cz': CZ,
            'da': DA,
            'db': DB,
            'dblassX': DBlassX,
            'dc': DC,
            'dz': DZ,
            'timestamp': time_model,
        }
    },
    'PSUB2': {
        'behaviors': {
        },
        'states': {
            'ca': CA,
            'cb': CB,
            'cblassX': CBlassX,
            'cc': CC,
            'cz': CZ,
            'da': DA,
            'db': DB,
            'dblassX': DBlassX,
            'dc': DC,
            'dz': DZ,
        }
    },
    'PSUB3': {
        'behaviors': {
        },
        'states': {
            'ca': CA,
            'cb': CB,
            'cblassX': CBlassX,
            'cc': CC,
            'cz': CZ,
            'da': DA,
            'db': DB,
            'dblassX': DBlassX,
            'dc': DC,
            'dz': DZ,
        }
    }
}

sim_config = config_sim({
    "N": 2,
    "T": range(4)
})

append_configs(sim_config, state_dict, {}, {}, {}, partial_state_update_blocks)
