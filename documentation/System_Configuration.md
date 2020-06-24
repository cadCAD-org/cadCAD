# [System Configuration:](https://github.com/BlockScience/distroduce/blob/master/documentation/dist_exec_doc.ipynb) 


## Conversions
##### Note: The following applies as a result of simulation execution

#### System Configurations as List of Configuration Objects
```python
fmt_configs = configs_as_objs(configs)
pprint(fmt_configs)
print()
pprint(fmt_configs[0].sim_config)
```
Return:
```
[<cadCAD.configuration.Configuration object at 0x116a21b90>,
 <cadCAD.configuration.Configuration object at 0x116a21c90>]

{'M': {'alpha': 1, 'beta': 2, 'gamma': 3, 'omega': 7},
 'N': 2,
 'T': range(0, 10),
 'run_id': 1,
 'simulation_id': 0}
```

#### System Configurations as a Pandas DataFrame
```python
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
