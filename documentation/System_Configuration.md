# Display System Model Configurations:

## Announcement:

See [CHANGELOG](CHANGELOG.md)

The `configs` (System Model Configurations) `list` has been **temporarily** flattened to contain single run 
`Configuration` objects to support elastic workloads. This functionality will be restored in a subsequent release by a 
class that returns `configs`'s original representation in ver. `0.3.1`.
* The conversion utilities have been provided to restore its original representation of configurations with 
runs >= 1
    * System Configuration Conversions:
        * Configuration as List of Configuration Objects (as in ver. `0.3.1`) 
        * New: System Configuration as a Pandas DataFrame
        * New: System Configuration as List of Dictionaries

## Conversions
##### Note: The following applies as a result of simulation execution

#### Imports:
```python
from cadCAD.configuration.utils import configs_as_objs, configs_as_dataframe, configs_as_dicts
```

#### System Configurations as List of Configuration Objects
Example:
* `configs` is temporarily returned in a flattened format and reformatted into its intended format. 
* `Configuration` objects at `0x10790e470` and `0x1143dd630` are reconstituted into objects at `0x10790e7b8` 
and `0x116268908` respectively.
```python
from cadCAD import configs
flattened_configs = configs
         
print('Flattened Format: Temporary')  
pprint(flattened_configs)
print()

print('Intended Format:')
intended_configs = configs_as_objs(flattened_configs)
pprint(intended_configs)
print()

print("Object: cadCAD.configuration.Configuration(...).sim_config")
pprint(intended_configs[0].sim_config)
print()
```
Return:
```
Flattened Format: Temporary
[<cadCAD.configuration.Configuration object at 0x10790e470>,
 <cadCAD.configuration.Configuration object at 0x10790e7b8>,
 <cadCAD.configuration.Configuration object at 0x1143dd630>,
 <cadCAD.configuration.Configuration object at 0x116268908>]

Intended Format:
[<cadCAD.configuration.Configuration object at 0x10790e7b8>,
 <cadCAD.configuration.Configuration object at 0x116268908>]

Object: cadCAD.configuration.Configuration(...).sim_config
{'M': [{}],
 'N': 2,
 'T': range(0, 1),
 'run_id': 1,
 'simulation_id': 0,
 'subset_id': 0,
 'subset_window': deque([0, None], maxlen=2)}
```

#### System Configurations as a Pandas DataFrame
```python
flattened_configs = configs
configs_df = configs_as_dataframe(configs)
configs_df
```

#### System Configurations as List of Dictionaries
```python
configs_dicts: list = configs_as_dicts(configs)
pprint(configs_dicts[0]['sim_config'])
```
Return:
```
{'env_processes': {'s3': [<function <lambda> at 0x7f8f9c99bd90>,
                          <function <lambda> at 0x7f8f9c9a11e0>],
                   's4': <function env_trigger.<locals>.trigger.<locals>.env_update at 0x7f8f9c9a12f0>},
 'exogenous_states': {},
 'initial_state': {'s1': 0.0,
                   's2': 0.0,
                   's3': 1.0,
                   's4': 1.0,
                   'timestamp': '2018-10-01 15:16:24'},
 'kwargs': {},
 'partial_state_updates': [{'policies': {'p1': <function p1m1 at 0x7f8f9c985ea0>,
                                         'p2': <function p2m1 at 0x7f8f9c985f28>},
                            'variables': {'s1': <function s1m1 at 0x7f8f9c99b268>,
                                          's2': <function s2m1 at 0x7f8f9c99b2f0>,
                                          's3': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99bae8>,
                                          's4': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99bea0>,
                                          'timestamp': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99b730>}},
                           {'policies': {'p1': <function p1m2 at 0x7f8f9c99b048>,
                                         'p2': <function p2m2 at 0x7f8f9c99b0d0>},
                            'variables': {'s1': <function s1m2 at 0x7f8f9c99b378>,
                                          's2': <function s2m2 at 0x7f8f9c99b400>,
                                          's3': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99bbf8>,
                                          's4': <function var_trigger.<locals>.<lambda> at 0x7f8f9c9a1048>,
                                          'timestamp': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99b840>}},
                           {'policies': {'p1': <function p1m3 at 0x7f8f9c99b158>,
                                         'p2': <function p2m3 at 0x7f8f9c99b1e0>},
                            'variables': {'s1': <function s1m3 at 0x7f8f9c99b488>,
                                          's2': <function s2m3 at 0x7f8f9c99b510>,
                                          's3': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99bd08>,
                                          's4': <function var_trigger.<locals>.<lambda> at 0x7f8f9c9a1158>,
                                          'timestamp': <function var_trigger.<locals>.<lambda> at 0x7f8f9c99b950>}}],
 'policy_ops': [<function <lambda> at 0x7f8f9cb39158>],
 'run_id': 249,
 'seeds': {'a': <mtrand.RandomState object at 0x7f8f9c9a21f8>,
           'b': <mtrand.RandomState object at 0x7f8f9c9a2240>,
           'c': <mtrand.RandomState object at 0x7f8f9c9a2288>,
           'z': <mtrand.RandomState object at 0x7f8f9ca04948>},
 'session_id': 'cadCAD_user=0_249',
 'sim_config': {'M': {'alpha': 1, 'beta': 2, 'gamma': 3, 'omega': 7},
                'N': 250,
                'T': range(0, 5000),
                'run_id': 249,
                'simulation_id': 0},
 'simulation_id': 0,
 'user_id': 'cadCAD_user'}
```
