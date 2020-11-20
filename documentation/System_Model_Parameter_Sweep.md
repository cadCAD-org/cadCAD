System Model Parameter Sweep
==
Parametrization of a System Model configuration that produces multiple configurations.

##### Set Parameters
*Note:* `M` values require up to a maximum of 2 distinct lengths
```python
M = {
    'alpha': [1],
    'beta': [2, 5],
    'gamma': [3, 4],
    'omega': [7]
}
```
The parameters above produce 2 simulations.
* Simulation 1: 
    * `alpha = 1`
    * `beta = 2`
    * `gamma = 3`
    * `omega = 7`
* Simulation 2:
    * `alpha = 1`
    * `beta = 5`
    * `gamma = 4`
    * `omega = 7`

All parameters can also be set to include a single parameter each, which will result in a single simulation.

##### Example State Updates

Previous State:
`y = 0`

```python
def state_update(_params, step, sH, s, _input, **kwargs):
    y = 'state'
    x = s['state'] + _params['alpha'] + _params['gamma']
    return y, x
```
* Updated State:
    * Simulation 1: `y = 4 = 0 + 1 + 3` 
    * Simulation 2: `y = 5 = 0 + 1 + 4`

##### Example Policy Updates
```python
# Internal States per Mechanism
def policies(_params, step, sH, s, **kwargs):
    return {'beta': _params['beta'], 'gamma': _params['gamma']}
```
* Simulation 1: `{'beta': 2, 'gamma': 3]}` 
* Simulation 2: `{'beta': 5, 'gamma': 4}`

##### Configure Simulation
```python
from cadCAD.configuration.utils import config_sim

g = {
    'alpha': [1],
    'beta': [2, 5],
    'gamma': [3, 4],
    'omega': [7]
}

sim_config = config_sim(
    {
        "N": 2,
        "T": range(5),
        "M": g,
    }
)
```
#### Example
##### * [System Model Configuration](examples/param_sweep.py)