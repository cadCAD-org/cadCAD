Policy Aggregation
==

For each Partial State Update, multiple policy dictionaries are aggregated into a single dictionary to be imputted into 
all state functions using an initial reduction function and optional subsequent map functions. 

#### Aggregate Function Composition:
```python
# Reduce Function
add = lambda a, b: a + b # Used to add policy values of the same key
# Map Function
mult_by_2 = lambda y: y * 2 # Used to multiply all policy values by 2
policy_ops=[add, mult_by_2]
```

##### Example Policy Updates per Partial State Update (PSU)
```python
def p1_psu1(_g, step, sL, s):
    return {'policy1': 1}
def p2_psu1(_g, step, sL, s):
    return {'policy2': 2}
```
* `add` not applicable due to lack of redundant policies
* `mult_by_2` applied to all policies
* Result: `{'policy1': 2, 'policy2': 4}`

```python
def p1_psu2(_g, step, sL, s):
    return {'policy1': 2, 'policy2': 2}
def p2_psu2(_g, step, sL, s):
    return {'policy1': 2, 'policy2': 2}
```
* `add` applicable due to redundant policies
* `mult_by_2` applied to all policies
* Result: `{'policy1': 8, 'policy2': 8}`

```python
def p1_psu3(_g, step, sL, s):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}
def p2_psu3(_g, step, sL, s):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}
```
* `add` applicable due to redundant policies
* `mult_by_2` applied to all policies
* Result: `{'policy1': 4, 'policy2': 8, 'policy3': 12}`

#### Aggregate Policies using functions
```python
from cadCAD.configuration import append_configs

append_configs(
    sim_configs=???,
    initial_state=???,
    partial_state_update_blocks=???,
    policy_ops=[add, mult_by_2] # Default: [lambda a, b: a + b]
)
```

#### [Example Configuration](link)
#### [Example Results](link)