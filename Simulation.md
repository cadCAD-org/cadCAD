# SimCAD Documentation

## Introduction

A blockchain is a distributed ledger with economic agents transacting in a network. The state of the network evolves with every new transaction, which can be a result of user behaviors, protocol-defined system mechanisms, or external processes.

It is not uncommon today for blockchain projects to announce a set of rules for their network and make claims about their system level behvaior. However, the validity of those claims is hardly validated. Furthermore, it is difficult to know the potential system-level impact when the network is considering an upgrade to their system rules and prameters.

To rigorously and reliably analyze, design, and improve cryptoeconomic networks, we are introducing this Computer Aided Design Engine where we define a cryptoeconomic network with its state and exogneous variables, model transactions as a result of agent behaviors, state mechanisms, and environmental processes. We can then run simulations with different initial states, mechanisms, environmental processes to understand and visualize network behavior under different conditions.

## State Variables and Transitions

We now define variables and different transition mechanisms that will be inputs to the simulation engine.

- ***State variables*** are defined to capture the shape and property of the network, such as a vector or a dictionary that captures all user balances.
- ***Exogenous variables*** are variables that represent external input and signal. They are only affected by environmental processes and are not affected by system mechanisms. Nonetheless, exgoneous variables can be used as an input to a mechanism that impacts state variables. They can be considered as read-only variables to the system.
- ***Behaviors per transition*** model agent behaviors in reaction to state variables and exogenous variables. The resulted user action will become an input to state mechanisms. Note that user behaviors should not directly update value of state variables. 
- ***State mechanisms per transition*** are system defined mechanisms that take user actions and other states as inputs and produce updates to the value of state variables.
- ***Exogenous state updates*** specify how exogenous variables evolve with time which can indirectly impact state variables through behavior and state mechanisms.
- ***Environmental processes*** model external changes that directly impact state or exogenous variables at specific timestamps or conditions. 

A state evolves to another state via state transition. Each transition is composed of behavior and state mechanisms as functions of state and exogenous variables. A flow of the state transition is as follows.

Given some state and exogenous variables of the system at the onset of a state transition, agent behavior takes in these variables as input and return a set of agent actions. This models after agent behavior and reaction to a set of variables. Given these agent actions, state mechanism, as defined by the protocol, takes these actions, state, and exogenous variables as inputs and return a new set of state variables.

## System Configuration File

Simulation engine takes in system configuration files, e.g. `config.py`, where all the above variables and mechanisms are defined. The following import statements should be added at the beginning of the configuration files.
```python
from decimal import Decimal
import numpy as np
from datetime import timedelta

from SimCAD import configs
from SimCAD.configuration import Configuration
from SimCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, \
    ep_time_step
```

State variables and their initial values can be defined as follows. Note that `timestamp` is a required field for this iteration of SimCAD for `env_proc` to work. Future iterations will strive to make this more generic and timestamp optional.
```python
genesis_dict = {
    's1': Decimal(0.0),
    's2': Decimal(0.0),
    's3': Decimal(1.0),
    'timestamp': '2018-10-01 15:16:24'
}
```

Each potential transition and its state and behavior mechanisms can be defined in the following dictionary object.
```python
transitions = {
    "m1": {
        "behaviors": {
            "b1": b1m1,
            "b2": b2m1
        },
        "states": {
            "s1": s1m1,
            "s2": s2m1
        }
    },
    "m2": {...}
}
```
Every behavior per transition should return a dictionary as actions taken by the agents. They will then be aggregated through addition in this version of SimCAD. Some examples of behaviors per transition are as follows. More flexible and user-defined aggregation functions will be introduced in future iterations but no example is provided at this point. 
```python
def b1m1(step, sL, s):
    return {'param1': 1}

def b1m2(step, sL, s):
    return {'param1': 'a', 'param2': 2}

def b1m3(step, sL, s):
    return {'param1': ['c'], 'param2': np.array([10, 100])}
```
State mechanism per transition on the other hand takes in the output of behavior mechanisms (`_input`) and returns a tuple of the name of the variable and the new value for the variable. Some examples of a state mechanism per transition are as follows. Note that each state mechanism is supposed to change one state variable at a time. Changes to multiple state variables should be done in separate mechanisms.
```python
def s1m1(step, sL, s, _input):
    y = 's1'
    x = _input['param1'] + 1
    return (y, x)

def s1m2(step, sL, s, _input):
    y = 's1'
    x = _input['param1']
    return (y, x)
```
Exogenous state update functions, for example `es3p1`, `es4p2` and `es5p2` below, update exogenous variables at every timestamp. Note that every timestamp is consist of all behaviors and state mechanisms in the order defined in `transitions` dictionary. If `exo_update_per_ts` is not used, exogenous state updates will be applied at every mechanism step (`m1`, `m2`, etc). Otherwise, exogenous state updates will only be applied once for every timestamp after all the mechanism steps are executed.
```python
exogenous_states = exo_update_per_ts(
    {
    "s3": es3p1,
    "s4": es4p2,
    "timestamp": es5p2
    }
)
```
To model randomness, we should also define pseudorandom seeds in the configuration as follows.
```python
seed = {
    'z': np.random.RandomState(1),
    'a': np.random.RandomState(2),
    'b': np.random.RandomState(3),
    'c': np.random.RandomState(3)
}
```
SimCAD currently supports generating random number from a normal distribution through `bound_norm_random` with `min` and `max` values specified. Examples of environmental processes with randomness are as follows. We also define timestamp format with `ts_format` and timestamp changes with `t_delta`. Users can define other distributions to update exogenous variables.
```python
proc_one_coef_A = 0.7
proc_one_coef_B = 1.3

def es3p1(step, sL, s, _input):
    y = 's3'
    x = s['s3'] * bound_norm_random(seed['a'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

def es4p2(step, sL, s, _input):
    y = 's4'
    x = s['s4'] * bound_norm_random(seed['b'], proc_one_coef_A, proc_one_coef_B)
    return (y, x)

ts_format = '%Y-%m-%d %H:%M:%S'
t_delta = timedelta(days=0, minutes=0, seconds=1)
def es5p2(step, sL, s, _input):
    y = 'timestamp'
    x = ep_time_step(s, s['timestamp'], fromat_str=ts_format, _timedelta=t_delta)
    return (y, x)
```
User can also define specific external events such as market shocks at specific timestamps through `env_processes` with `proc_trigger`. An environmental process with no `proc_trigger` will be called at every timestamp. In the example below, it will return the value of `s3` at every timestamp. Logical event triggers, such as a big draw down in exogenous variables, will be supported in a later version of SimCAD. 
```python
def env_a(x):
    return x
def env_b(x):
    return 10

env_processes = {
    "s3": env_a,
    "s4": proc_trigger('2018-10-01 15:16:25', env_b)
}
```

Lastly, we set the overall simulation configuration and initialize the `Configuration` class with the following. `T` denotes the time range and `N` refers to the number of simulation runs. Each run will start from the same initial states and run for `T` time range. Every transition is consist of behaviors, state mechanisms, exogenous updates, and potentially environmental processes. All of these happen within one time step in the simulation.
```python
sim_config = {
    "N": 2,
    "T": range(5)
}

configs.append(Configuration(sim_config, state_dict, seed, exogenous_states, env_processes, mechanisms))
```
