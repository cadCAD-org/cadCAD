Policy Aggregation
==

For each Partial State Update, multiple policy dictionaries are aggregated into a single dictionary to be inputted into 
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
def p1_psu1(_params, step, sH, s, **kwargs):
    return {'policy1': 1}
def p2_psu1(_params, step, sH, s, **kwargs):
    return {'policy2': 2}
```
* `add` not applicable due to lack of redundant policies
* `mult_by_2` applied to all policies
* Result: `{'policy1': 2, 'policy2': 4}`

```python
def p1_psu2(_params, step, sH, s, **kwargs):
    return {'policy1': 2, 'policy2': 2}
def p2_psu2(_params, step, sH, s, **kwargs):
    return {'policy1': 2, 'policy2': 2}
```
* `add` applicable due to redundant policies
* `mult_by_2` applied to all policies
* Result: `{'policy1': 8, 'policy2': 8}`

```python
def p1_psu3(_params, step, sH, s, **kwargs):
    return {'policy1': 1, 'policy2': 2, 'policy3': 3}
def p2_psu3(_params, step, sH, s, **kwargs):
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

#### Example
##### * [System Model Configuration](examples/policy_aggregation.py)
##### * Simulation Results:
```
+----+---------------------------------------------+-------+------+-----------+------------+
|    | policies                                    |   run |   s1 |   substep |   timestep |
|----+---------------------------------------------+-------+------+-----------+------------|
|  0 | {}                                          |     1 |    0 |         0 |          0 |
|  1 | {'policy1': 2, 'policy2': 4}                |     1 |    1 |         1 |          1 |
|  2 | {'policy1': 8, 'policy2': 8}                |     1 |    2 |         2 |          1 |
|  3 | {'policy3': 12, 'policy1': 4, 'policy2': 8} |     1 |    3 |         3 |          1 |
|  4 | {'policy1': 2, 'policy2': 4}                |     1 |    4 |         1 |          2 |
|  5 | {'policy1': 8, 'policy2': 8}                |     1 |    5 |         2 |          2 |
|  6 | {'policy3': 12, 'policy1': 4, 'policy2': 8} |     1 |    6 |         3 |          2 |
|  7 | {'policy1': 2, 'policy2': 4}                |     1 |    7 |         1 |          3 |
|  8 | {'policy1': 8, 'policy2': 8}                |     1 |    8 |         2 |          3 |
|  9 | {'policy3': 12, 'policy1': 4, 'policy2': 8} |     1 |    9 |         3 |          3 |
+----+---------------------------------------------+-------+------+-----------+------------+
```
