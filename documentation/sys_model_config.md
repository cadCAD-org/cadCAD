System Model Configuration
==

#### Introduction

Given System Model Configurations, cadCAD produces system event datasets that conform to specified system metrics. Each
event / record is of [Enogenous State variables](link) produced by user defined [Partial State Updates](link) (PSU / 
functions that update state); A sequence of event / record subsets that comprises the resulting system event dataset is 
produced by a [Partial State Update Block](link) (PSUB / a Tensor Field for which State, Policy, and Time are dimensions 
and PSU functions are values).

A **System Model Configuration** is comprised of a simulation configuration, initial endogenous states, Partial State 
Update Blocks, environmental process, and a user defined policy aggregation function.

Execution:

#### Simulation Properties

###### System Metrics
The following system metrics determine the size of resulting system event datasets:
* `run` - the number of simulations in the resulting dataset
* `timestep` - the number of timestamps in the resulting dataset
* `substep` - the number of PSUs per `timestep` / within PSUBS
* Number of events / records: `run` x `timestep` x `substep`

###### Simulation Configuration
For the following dictionary, `T` is assigned a `timestep` range, `N` is assigned the number of simulation runs, and 
`params` is assigned the [**Parameter Sweep**](link) dictionary.

```python
from cadCAD.configuration.utils import config_sim

sim_config = config_sim({
    "N": 2,
    "T": range(5),
    "M": params, # Optional
})
```

#### Initial Endogenous States 
**Enogenous State variables** are read-only variables defined to capture the shape and property of the network and 
represent internal input and signal. 

The PSUB tensor field is applied to the following states to produce a resulting system event 
dataset.
```python
genesis_states = {
    's1': 0.0,
    's2': 0.0,
    's3': 1.0,
    'timestamp': '2018-10-01 15:16:24'
}
```

#### Partial State Update Block:
- ***Partial State Update Block(PSUB)*** ***(Define ?)*** Tensor Field for which State, Policy, Time are dimensions 
and Partial State Update functions are values. 
- ***Partial State Update (PSU)*** are user defined functions that encodes state updates and are executed in 
a specified order PSUBs. PSUs update states given the most recent set of states and PSU policies.
- ***Mechanism*** ***(Define)***


The PSUBs is a list of PSU dictionaries of the structure within the code block below. PSUB elements (PSU dictionaries) 
are listed / defined in order of `substeps` and **identity functions** (returning a previous state's value) are assigned 
to unreferenced states within PSUs. The number of records produced produced per `timestep` is the number of `substeps`.

```python
partial_state_update_block = [
    {
        "policies": {
            "b1": p1_psu1,
            "b2": p2_psu1
        },
        "variables": {
            "s1": s1_psu1,
            "s2": s2_psu1
        }
    },
    {
        "policies": {
            "b1": p1_psu2,
        },
        "variables": {
            "s2": s2_psu2
        }
    },
    {...}
]
```
*Notes:* 
1. An identity function (returning the previous state value) is assigned to `s1` in the second PSU.
2. Currently the only names that need not correspond to the convention below are `'b1'` and `'b2'`.

#### Policies
- ***Policies*** ***(Define)*** When are policies behavior ?
- ***Behaviors*** model agent behaviors in reaction to state variables and exogenous variables. The 
resulted user action will become an input to PSUs. Note that user behaviors should not directly update value 
of state variables. 

Policies accept parameter sweep variables [see link] `_g` (`dict`), the most recent 
`substep` integer, the state history[see link] (`sH`), the most recent state record `s` (`dict) as inputs and returns a 
set of actions (`dict`).

Policy functions return dictionaries as actions. Policy functions provide access to parameter sweep variables [see link]
via dictionary `_g`.
```python
def p1_psu1(_g, substep, sH, s):
    return {'policy1': 1}
def p2_psu1(_g, substep, sH, s):
    return {'policy1': 1, 'policy2': 4}
```
For each PSU, multiple policy dictionaries are aggregated into a single dictionary to be imputted into 
all state functions using an initial reduction function (default: `lambda a, b: a + b`) and optional subsequent map 
functions. 
Example Result: `{'policy1': 2, 'policy2': 4}`

#### State Updates
State update functions provide access to parameter sweep variables [see link] `_g` (`dict`), the most recent `substep` 
integer, the state history[see link] (`sH`), the most recent state record as a dictionary (`s`), the policies of a 
PSU (`_input`), and returns a tuple of the state variable's name and the resulting new value of the variable. 

```python
def state_update(_g, substep, sH, s, _input):
    ...
    return state, update
```
**Note:** Each state update function updates one state variable at a time. Changes to multiple state variables requires 
separate state update functions. A generic example of a PSU is as follows. 

* ##### Endogenous State Updates
They are only updated by PSUs and can be used as inputs to a PSUs. 
```python
def s1_update(_g, substep, sH, s, _input):
    x = _input['policy1'] + 1
    return 's1', x

def s2_update(_g, substep, sH, s, _input):
    x = _input['policy2']
    return 's2', x
```

* ##### Exogenous State Updates
***Exogenous State variables*** ***(Review)*** are read-only variables that represent external input and signal. They
update endogenous states and are only updated by environmental processes. Exgoneous variables can be used 
as an input to a PSU that impacts state variables. ***(Expand upon Exogenous state updates)***

```python   
from datetime import timedelta
from cadCAD.configuration.utils import time_step
def es3_update(_g, substep, sH, s, _input): 
    x = ... 
    return 's3'
def es4_update(_g, substep, sH, s, _input): 
    x = ... 
    return 's4', x
def update_timestamp(_g, substep, sH, s, _input):
    x = time_step(dt_str=s[y], dt_format='%Y-%m-%d %H:%M:%S', _timedelta=timedelta(days=0, minutes=0, seconds=1))
    return 'timestamp', x
```
Exogenous state update functions (`es3_update`, `es4_update` and `es5_update`) update once per timestamp and should be 
included as a part of the first PSU in the PSUB. 
```python
partial_state_update_block['psu1']['variables']['s3'] = es3_update
partial_state_update_block['psu1']['variables']['s4'] = es4_update
partial_state_update_block['psu1']['variables']['timestamp'] = update_timestamp
```

* #### Environmental Process
- ***Environmental processes*** model external changes that directly impact exogenous states at given specific 
conditions such as market shocks at specific timestamps.

Create a dictionary like `env_processes` below for which the keys are exogenous states and the values are lists of user
defined **Environment Update** functions to be composed (e.g. `[f(params, x), g(params, x)]` becomes 
`f(params, g(params, x))`).

Environment Updates accept the [**Parameter Sweep**](link) dictionary `params` and a state as a result of a PSU.
```python
def env_update(params, state):
    . . .
    return updated_state
    
# OR 

env_update = lambda params, state: state + 5
```

The `env_trigger` function is used to apply composed environment update functions to a list of specific exogenous state
update results. `env_trigger` accepts the total number of `substeps` for the simulation / `end_substep` and returns a 
function accepting `trigger_field`, `trigger_vals`, and `funct_list`.

In the following example functions are used to add `5` to every `s3` update and assign `10` to `s4` at
`timestamp`s `'2018-10-01 15:16:25'`, `'2018-10-01 15:16:27'`, and `'2018-10-01 15:16:29'`. 
```python
from cadCAD.configuration.utils import env_trigger
trigger_timestamps = ['2018-10-01 15:16:25', '2018-10-01 15:16:27', '2018-10-01 15:16:29']
env_processes = {
    "s3": [lambda params, x: x + 5],
    "s4": env_trigger(end_substep=3)(
        trigger_field='timestamp', trigger_vals=trigger_timestamps, funct_list=[lambda params, x: 10]
    )
}
```

#### System Model Configuration
`append_configs`, stores a **System Model Configuration** to be (Executed)[url] as 
simulations producing system event dataset(s)

```python
from cadCAD.configuration import append_configs

append_configs(
    sim_configs=sim_config,
    initial_state=genesis_states,
    env_processes=env_processes,
    partial_state_update_blocks=partial_state_update_block,
    policy_ops=[lambda a, b: a + b]
)
```

#### [System Simulation Execution](link)
