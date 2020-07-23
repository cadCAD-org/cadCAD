Simulation Configuration
==

## Introduction

Given a **Simulation Configuration**, cadCAD produces datasets that represent the evolution of the state of a system 
over [discrete time](https://en.wikipedia.org/wiki/Discrete_time_and_continuous_time#Discrete_time). The state of the 
system is described by a set of [State Variables](#State-Variables). The dynamic of the system is described by 
[Policy Functions](#Policy-Functions) and [State Update Functions](#State-Update-Functions), which are evaluated by 
cadCAD according to the definitions set by the user in [Partial State Update Blocks](#Partial-State-Update-Blocks).

A Simulation Configuration is comprised of a [System Model](#System-Model) and a set of 
[Simulation Properties](#Simulation-Properties).

`append_configs`, stores a **Simulation Configuration** to be [Executed](/JS4Q9oayQASihxHBJzz4Ug) by cadCAD

```python
from cadCAD.configuration import append_configs

append_configs(
    user_id = ..., # OPTIONAL: cadCAD Session User ID
    initial_state = ..., # System Model
    partial_state_update_blocks = ..., # System Model
    policy_ops = ..., # System Model
    sim_configs = ... # Simulation Properties
)
```
Parameters:
* **user_id** : str - OPTIONAL: cadCAD Session User ID
* **initial_state** : _dict_ - [State Variables](#State-Variables) and their initial values
* **partial_state_update_blocks** : List[dict[dict]] - List of [Partial State Update Blocks](#Partial-State-Update-Blocks)
* **policy_ops** : List[functions] - See [Policy Aggregation](Policy_Aggregation.md) 
* **sim_configs** - See [System Model Parameter Sweep](System_Model_Parameter_Sweep.md)

## Simulation Properties

Simulation properties are passed to `append_configs` in the `sim_configs` parameter. To construct this parameter, we 
use the `config_sim` function in `cadCAD.configuration.utils`

```python
from cadCAD.configuration import append_configs
from cadCAD.configuration.utils import config_sim

sim_config_dict = {
    "N": ...,
    "T": range(...),
    "M": ...
}

c = config_sim(sim_config_dict)

append_configs(
    ...
    sim_configs = c # Simulation Properties
)
```

### T - Simulation Length
Computer simulations run in discrete time:

>Discrete time views values of variables as occurring at distinct, separate "points in time", or equivalently as being 
unchanged throughout each non-zero region of time ("time period")—that is, time is viewed as a discrete variable. (...) 
This view of time corresponds to a digital clock that gives a fixed reading of 10:37 for a while, and then jumps to a 
new fixed reading of 10:38, etc. 
([source: Wikipedia](https://en.wikipedia.org/wiki/Discrete_time_and_continuous_time#Discrete_time))

As is common in many simulation tools, in cadCAD too we refer to each discrete unit of time as a **timestep**. cadCAD 
increments a "time counter", and at each step it updates the state variables according to the equations that describe 
the system.

The main simulation property that the user must set when creating a Simulation Configuration is the number of timesteps 
in the simulation. In other words, for how long do they want to simulate the system that has been modeled.

### N - Number of Runs

cadCAD facilitates running multiple simulations of the same system sequentially, reporting the results of all those 
runs in a single dataset. This is especially helpful for running 
[Monte Carlo Simulations](../tutorials/robot-marbles-part-4/robot-marbles-part-4.ipynb).

### M - Parameters of the System

Parameters of the system, passed to the state update functions and the policy functions in the `params` parameter are 
defined here. See [System Model Parameter Sweep](/4oJ_GT6zRWW8AO3yMhFKrg) for more information.

## System Model
The System Model describes the system that will be simulated in cadCAD. It is comprised of a set of 
[State Variables](##State-Variables) and the [State Update Functions](#State-Update-Functions) that determine the 
evolution of the state of the system over time. [Policy Functions](#Policy-Functions) (representations of user policies 
or internal system control policies) may also be part of a System Model.

### State Variables
>A state variable is one of the set of variables that are used to describe the mathematical "state" of a dynamical 
system. Intuitively, the state of a system describes enough about the system to determine its future behaviour in the 
absence of any external forces affecting the system. ([source: Wikipedia](https://en.wikipedia.org/wiki/State_variable))

cadCAD can handle state variables of any Python data type, including custom classes. It is up to the user of cadCAD to 
determine the state variables needed to **sufficiently and accurately** describe the system they are interested in.

State Variables are passed to `append_configs` along with its initial values, as a Python `dict` where the `dict_keys` 
are the names of the variables and the `dict_values` are their initial values.

```python
from cadCAD.configuration import append_configs

genesis_states = {
    'state_variable_1': 0,
    'state_variable_2': 0,
    'state_variable_3': 1.5,
    'timestamp': '2019-01-01 00:00:00'
}

append_configs(
    initial_state = genesis_states,
    ...
)
```
### State Update Functions
State Update Functions represent equations according to which the state variables change over time. Each state update 
function must return a tuple containing a string with the name of the state variable being updated and its new value. 
Each state update function can only modify a single state variable. The general structure of a state update function is:
```python
def state_update_function_A(_params, substep, sH, s, _input, **kwargs):
    ...
    return 'state_variable_name', new_value
```
Parameters:
* **_params** : _dict_ - [System parameters](/4oJ_GT6zRWW8AO3yMhFKrg)
* **substep** : _int_ - Current [substep](#Substep)
* **sH** : _list[list[dict_]] - Historical values of all state variables for the simulation. See 
[Historical State Access](/smiyQTnATtC9xPwvF8KbBQ) for details
* **s** : _dict_ - Current state of the system, where the `dict_keys` are the names of the state variables and the 
`dict_values` are their current values.
* **_input** : _dict_ - Aggregation of the signals of all policy functions in the current 
[Partial State Update Block](#Partial-State-Update-Block)
* **\*\*kwargs** - State Update feature extensions 

Return:
* _tuple_ containing a string with the name of the state variable being updated and its new value.
    
State update functions should not modify any of the parameters passed to it, as those are mutable Python objects that 
cadCAD relies on in order to run the simulation according to the specifications.

### Policy Functions
A Policy Function computes one or more signals to be passed to [State Update Functions](#State-Update-Functions) 
(via the _\_input_ parameter). Read 
[this article](../tutorials/robot-marbles-part-2/robot-marbles-part-2.ipynb) 
for details on why and when to use policy functions.

<!-- We would then expand the tutorials with these kind of concepts
#### Policies
Policies consist of the potential action made available through mechanisms. The action taken is expected to be the 
result of a conditional determination of the past state.  

While executed the same, the modeller can approach policies dependent on the availability of a mechanism to a population.

- ***Control Policy***
When the controlling or deploying entity has the ability to act in order to affect some aspect of the system, this is a 
control policy.
- ***User Policy*** model agent behaviors in reaction to state variables and exogenous variables. The resulted user 
action will become an input to PSUs. Note that user behaviors should not directly update value of state variables. 
The action taken, as well as the potential to act, through a mechanism is a behavior.  -->

The general structure of a policy function is:
```python
def policy_function_1(_params, substep, sH, s, **kwargs):
    ...
    return {'signal_1': value_1, ..., 'signal_N': value_N}
```
Parameters:
* **_params** : _dict_ - [System parameters](/4oJ_GT6zRWW8AO3yMhFKrg)
* **substep** : _int_ - Current [substep](#Substep)
* **sH** : _list[list[dict_]] - Historical values of all state variables for the simulation. See 
[Historical State Access](/smiyQTnATtC9xPwvF8KbBQ) for details
* **s** : _dict_ - Current state of the system, where the `dict_keys` are the names of the state variables and the 
`dict_values` are their current values.
* **\*\*kwargs** - Policy Update feature extensions 
    
Return:
* _dict_ of signals to be passed to the state update functions in the same 
[Partial State Update Block](#Partial-State-Update-Blocks)

Policy functions should not modify any of the parameters passed to it, as those are mutable Python objects that cadCAD 
relies on in order to run the simulation according to the specifications.

At each [Partial State Update Block](#Partial-State-Update-Blocks) (PSUB), the `dicts` returned by all policy functions 
within that PSUB dictionaries are aggregated into a single `dict` using an initial reduction function 
(a key-wise operation, default: `dic1['keyA'] + dic2['keyA']`) and optional subsequent map functions. The resulting 
aggregated `dict` is then passed as the `_input` parameter to the state update functions in that PSUB. For more 
information on how to modify the aggregation method, see [Policy Aggregation](/63k2ncjITuqOPCUHzK7Viw).

### Partial State Update Blocks

A **Partial State Update Block** (PSUB) is a set of State Update Functions and Policy Functions such that State Update 
Functions in the set are independent from each other and Policies in the set are independent from each other and from 
the State Update Functions in the set. In other words, if a state variable is updated in a PSUB, its new value cannot 
impact the State Update Functions and Policy Functions in that PSUB - only those in the next PSUB.

![](https://i.imgur.com/9rlX9TG.png)

Partial State Update Blocks are passed to `append_configs` as a List of Python `dicts` where the `dict_keys` are named 
`"policies"` and `"variables"` and the values are also Python `dicts` where the keys are the names of the policy and 
state update functions and the values are the functions.

```python
PSUBs = [
    {
        "policies": {
            "b_1": policy_function_1,
            ...
            "b_J": policy_function_J
        },
        "variables": {
            "s_1": state_update_function_1,
            ...
            "s_K": state_update_function_K
        }
    }, #PSUB_1,
    {...}, #PSUB_2,
    ...
    {...} #PSUB_M
]

append_configs(
    ...
    partial_state_update_blocks = PSUBs,
    ...
)

```

#### Substep
At each timestep, cadCAD iterates over the `partial_state_update_blocks` list. For each Partial State Update Block, 
cadCAD returns a record containing the state of the system at the end of that PSUB. We refer to that subdivision of a 
timestep as a `substep`.

## Result Dataset

cadCAD returns a dataset containing the evolution of the state variables defined by the user over time, with three `int` 
indexes:
* `run` - id of the [run](#N-Number-of-Runs)
* `timestep` - discrete unit of time (the total number of timesteps is defined by the user in the 
[T Simulation Parameter](#T-Simulation-Length))
* `substep` - subdivision of timestep (the number of [substeps](#Substeps) is the same as the number of Partial State 
Update Blocks)

Therefore, the total number of records in the resulting dataset is `N` x `T` x `len(partial_state_update_blocks)`

#### [System Simulation Execution](Simulation_Execution.md)
