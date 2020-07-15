# Using cadCAD 0.4.17
(see below for [updating older projects](#Updating-older-projects))

## Use python3.6 through virtual environment (optional)
```
python3.6 -m venv venv
source venv/bin/activate
```

## Install cadCAD
`pip install cadCAD==0.4.17`

Verify:
```
$ pip freeze
cadCAD==0.4.17
dill==0.3.2
fn==0.4.3
funcy==1.14
multiprocess==0.70.10
numpy==1.19.0
pandas==1.0.5
pathos==0.2.6
pox==0.2.8
ppft==1.6.6.2
python-dateutil==2.8.1
pytz==2020.1
six==1.15.0
```

When initially using python 3.8, these packages: pathos, funcy, fn, dill, multiprocess, pox, ppft; had - `error: invalid command 'bdist_wheel'`
But looked to have still worked.

Additional python dependencies needed:
- `pip install jupyterlab`
- `pip install matplotlib`
- `pip install networkx`
- `pip install scipy`

# Updating older projects

In essense the core difference in upgrading to 0.4.17 is
in how `Configuration` objects are created and passed to the `Executor`. Also a few variations around use of the Executor.

## Configurations

## imports
```
from cadCAD.configuration.utils import config_sim
from cadCAD.configuration import append_configs
from cadCAD import configs
```

If no longer accessing a configuration directly, you can remove:

~~`from cadCAD.configuration import Configuration`~~

## Adding configurations

Rather than creating individual Configuration objects with:
  `config = Configuration(initial_state, partial_state_update_blocks, sim_config)`

Configurations are appended to the (imported) `configs` array via:
  `append_configs(initial_state, partial_state_update_blocks, sim_configs)`

Note `sim_configs` now takes an array.
And as per [docs](https://github.com/cadCAD-org/cadCAD/tree/master/documentation#simulation-properties) each element (dictionary) should be preprocessed with `config_sim()`

## Executor

The execution mode needs 3 changes:
- `ExecutionContext` mode names have changed, eg can replace `single_proc` with `local_mode`.
- `Executor` should be passed the `configs` array from above.
- finally, `sessions` are additionally when calling `execute()`

That is, this:
```
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config]) # Pass the configuration object inside an array
raw_result, tensor = executor.execute() # The `execute()` method returns a tuple; its first elements contains the raw results
```
Changes to:
```
exec_context = ExecutionContext(exec_mode.local_mode)\n",
executor = Executor(exec_context, configs) # Pass the configuration object inside an array\n",
raw_result, tensor, sessions = executor.execute() # The `execute()` method returns a tuple; its first elements contains the raw results"
```

### Executor results
The results now contain an additional key, `simulation`, which is incremented for each `sim_configs` dictionary element passed to `append_configs()`.


Note each config dictionary that has multiple runs (`N` > 1) will create multiple `Configuration` elements in the `configs` array, each with `N` = 1.

Per dictionary, the `simulation_id` will be shared in its corresponding `Configuration`objects. The results of `execute()` return this under `simulation`.
