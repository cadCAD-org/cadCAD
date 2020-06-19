Historical State Access (Alpha)
==
#### Motivation
The current state (values of state variables) is accessed through the `s` list. When the user requires previous state variable values, they may be accessed through the state history list, `sH`. Accessing the state history should be implemented without creating unintended feedback loops on the current state.

The 3rd parameter of state and policy update functions (labeled as `sH` of type `List[List[dict]]`) provides access to past Partial State Update Block (PSUB) given a negative offset number. `access_block` is used to access past PSUBs (`List[dict]`) from `sH`. For example, an offset of `-2` denotes the second to last PSUB.

#### Exclusion List
Create a list of states to exclude from the reported PSU.
```python
exclusion_list = [
    'nonexistent', 'last_x', '2nd_to_last_x', '3rd_to_last_x', '4th_to_last_x'
]
```
##### Example Policy Updates
###### Last partial state update
```python
def last_update(_params, substep, sH, s, **kwargs):
    return {"last_x": access_block(
            state_history=sH,
            target_field="last_x", # Add a field to the exclusion list
            psu_block_offset=-1,
            exculsion_list=exclusion_list
        )
    }
```
* Note: Although `target_field` adding a field to the exclusion may seem redundant, it is useful in the case of the exclusion list being empty while the `target_field` is assigned to a state or a policy key.
##### Define State Updates
###### 2nd to last partial state update
```python
def second2last_update(_params, substep, sH, s, **kwargs):
    return {"2nd_to_last_x": access_block(sH, "2nd_to_last_x", -2, exclusion_list)}
```


###### 3rd to last partial state update
```python
def third_to_last_x(_params, substep, sH, s, _input, **kwargs):
    return '3rd_to_last_x', access_block(sH, "3rd_to_last_x", -3, exclusion_list)
```
###### 4rd to last partial state update
```python
def fourth_to_last_x(_params, substep, sH, s, _input, **kwargs):
    return '4th_to_last_x', access_block(sH, "4th_to_last_x", -4, exclusion_list)
```
###### Non-exsistent partial state update
* `psu_block_offset >= 0` doesn't exist
```python
def nonexistent(_params, substep, sH, s, _input, **kwargs):
    return 'nonexistent', access_block(sH, "nonexistent", 0, exclusion_list)
```

#### [Example Simulation:](examples/historical_state_access.py)


#### Example Output:
###### State History
```
+----+-------+-----------+------------+-----+
|    |   run |   substep |   timestep |   x |
|----+-------+-----------+------------+-----|
|  0 |     1 |         0 |          0 |   0 |
|  1 |     1 |         1 |          1 |   1 |
|  2 |     1 |         2 |          1 |   2 |
|  3 |     1 |         3 |          1 |   3 |
|  4 |     1 |         1 |          2 |   4 |
|  5 |     1 |         2 |          2 |   5 |
|  6 |     1 |         3 |          2 |   6 |
|  7 |     1 |         1 |          3 |   7 |
|  8 |     1 |         2 |          3 |   8 |
|  9 |     1 |         3 |          3 |   9 |
+----+-------+-----------+------------+-----+
```
###### Accessed State History: 
Example: `last_x`
```
+----+-----------------------------------------------------------------------------------------------------------------------------------------------------+
|    | last_x                                                                                                                                              |
|----+-----------------------------------------------------------------------------------------------------------------------------------------------------|
|  0 | []                                                                                                                                                  |
|  1 | [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}]                                                                                                   |
|  2 | [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}]                                                                                                   |
|  3 | [{'x': 0, 'run': 1, 'substep': 0, 'timestep': 0}]                                                                                                   |
|  4 | [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}] |
|  5 | [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}] |
|  6 | [{'x': 1, 'run': 1, 'substep': 1, 'timestep': 1}, {'x': 2, 'run': 1, 'substep': 2, 'timestep': 1}, {'x': 3, 'run': 1, 'substep': 3, 'timestep': 1}] |
|  7 | [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}] |
|  8 | [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}] |
|  9 | [{'x': 4, 'run': 1, 'substep': 1, 'timestep': 2}, {'x': 5, 'run': 1, 'substep': 2, 'timestep': 2}, {'x': 6, 'run': 1, 'substep': 3, 'timestep': 2}] |
+----+-----------------------------------------------------------------------------------------------------------------------------------------------------+
```