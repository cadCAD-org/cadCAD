# Changelog:
### September 27, 2021
#### New Features:
* **ver. ≥ `0.4.28`:**
    * ##### [Experiments](documentation#experiments)
        * ##### [System Model Configurations]
          * Configurations (`cadCAD.utils.Configuration`'s) are now accessed via the `configs` member of `cadCAD.configuration.Experiment`.
            [Example:](documentation#experiments) `cadCAD.configuration.Experiment().configs`
          * `cadCAD.configs` has be re-included for backwards compatibility and has been assigned `cadCAD.experiment.configs`
        * ##### [Experiments]
          * `cadCAD.configuration.Experiment()` is unique representation of an experiment of one or more configured System 
          Models.
            * The `cadCAD` module now contains a default Experiment object `cadCAD.experiment` as an instantiation of 
                `cadCAD.configuration.Experiment()`
          * An `Experiment`'s `append_model` method stores multiple system model `Configuration`'s for simulation 
          execution within `cadCAD.configuration.Experiment().configs`.
          `cadCAD.configuration.Experiment().model_ids` contains system model labels and/or indexes for 
          `cadCAD.configuration.Experiment().configs`
              * The `Experiment`'s `append_model` method is defined with `model_id` parameter that accepts a system model 
              label.
                * If duplicate `model_id`'s are specified, an index is appended to the label after the `@` symbol.
                (Example: `cadCAD.configuration.Experiment().model_ids = ['sys_model', 'sys_model@1', 'sys_model@2', ...]`) 
                * If `model_id`'s are not specified or duplicate, the label is auto-generated as a string indicating the 
                system model index within `cadCAD.configuration.Experiment().configs`.
                (Example of unspecified system models at indexes 1, 3, and 4: 
                `cadCAD.configuration.Experiment().model_ids = ['sys_model', '1', 'sys_model@2', '3', '4', ...]`)
    * ##### [Upgrade Guide:](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/cadCAD-v0.4.28-Model-Upgrade-Guide.md) specific to feature changes / additions


### August 25, 2021
#### New Features:
* **ver. ≥ `0.4.27`:**
    * ##### [Experiments](documentation#experiments)
        * ##### [System Model Configurations]
          * Configurations (`cadCAD.utils.Configuration`'s) as are no longer a part of the `cadCAD` module 
            (as `cadCAD.configs`) and are now accessed via the `configs` member of `cadCAD.configuration.Experiment`.
            [Example:](documentation#experiments) `cadCAD.configuration.Experiment().configs`
        * ##### [Experiments]
          * `cadCAD.configuration.Experiment` is unique representation of an experiment of one or more configured System 
          Models. An `Experiment`'s `append_model` method stores multiple system model `Configuration`'s for simulation 
          execution.
              * The `Experiment`'s `append_model` method requires a `model_id` parameter that is auto-created as `'sys_model_#'`.
              * **Requirements:** 
                * Users must use different `model_id`'s when appending multiple System Model Configurations.
                * Users can no longer use the `config_list` method of `cadCAD.configuration.Experiment`
              * **Backwards Compatibility:** The `append_model` method of `cadCAD.configuration.Experiment` can also be used as 
                the `append_configs` method.
    * Removed [Nix](https://nixos.org/)
    * ##### [Upgrade Guide:](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/cadCAD-v0.4.27-Model-Upgrade-Guide.md) specific to feature changes / additions
* **Fixes:** 
    * [#248](https://github.com/cadCAD-org/cadCAD/issues/248)
        * The previous release was returning partial results. An A/B test for this has been included and will be for 
          future releases
    * [#242](https://github.com/cadCAD-org/cadCAD/issues/242)
        * Parallelized simulations enabled with the re-inclusion of `ProcessPool`.
    * [#257](https://github.com/cadCAD-org/cadCAD/issues/257)
        * ValueError for runs accepted by the `cadCAD.configuration.Experiment().append_model` via the `sim_configs` no
          longer gives mis-leading error message if catching a non-related ValueError
    * [#252](https://github.com/cadCAD-org/cadCAD/issues/252)
        * Jupyter lab and Jupyter notebook recognises cadCAD module

    
### September 22, 2020
##### [Multi - System Model Execution](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/Simulation_Execution.md#multiple-simulation-execution)
* **ver. ≥ `0.4.23`:**
    * **Hot-Fix:** [#203](https://github.com/cadCAD-org/cadCAD/pull/203) (**No Breaking Changes**)
        * Multi - System Model simulation results will no longer return truncated results (exclude the results of the last 
        `cadCAD.configuration.Configuration` appended to `cadCAD.configs`).
        * Issue: [#195](https://github.com/cadCAD-org/cadCAD/issues/195)
    * Parameter Sweep value `M` (Params) requires up to a maximum of 2 distinct lengths


### August 5, 2020
##### [Experiments](documentation#experiments)
* `cadCAD.configuration.Experiment` (Alpha) is in development and needed to be released to support the implementation of 
web applications and proprietary feature extensions. It is intended to represent a unique identifier of an experiment of 
one or more configured System Models. For this reason, `append_configs` is a method of 
`cadCAD.configuration.Experiment`. As of now it does not support multi - system model simulation because configurations 
are still appended globally despite `append_config` being a method of Experiment.

###### Examples:
* **ver. ≥ `0.4.22`:**
    ```python
    from cadCAD.configuration import Experiment
    exp = Experiment()
    exp.append_configs(...)
    ```
* **ver. `0.3.1`:** *Deprecated*
    ```python
    from cadCAD.configuration import append_configs
    append_configs(...)
    ```


### June 22, 2020
* Bug Fix: Multiprocessing error for Windows


### June 19, 2020
    
### New Features:
##### [Local Execution Mode (Default)](documentation/Simulation_Execution.md#simulation-execution-modes)
* Local Execution Mode (Default): Implicit parallelization of Monte-Carlo / Stochastic simulations (Automatically 
selects Multi-Threaded Mode if simulations are configured for more than a single run)
    * **Backwards Compatibility:** `cadCAD.engine.ExecutionMode` accepts legacy execution modes from ver. `0.3.1`
    
###### Examples:
* **ver. ≥ `0.4.22`:**
    ```python
    from cadCAD.engine import ExecutionMode, ExecutionContext
    exec_mode = ExecutionMode()
    local_ctx = ExecutionContext(context=exec_mode.local_mode)
    ```
* **ver. `0.3.1`:** 
    
    Multi-Threaded:
    ```python
    from cadCAD.engine import ExecutionMode, ExecutionContext
    
    exec_mode = ExecutionMode()
    single_ctx = ExecutionContext(context=exec_mode.multi_proc)
    ```
    
    Single-Thread:
    ```python
    from cadCAD.engine import ExecutionMode, ExecutionContext
  
    exec_mode = ExecutionMode()
    multi_ctx = ExecutionContext(context=exec_mode.single_proc)
    ```
        

##### cadCAD Post-Processing Enhancements / Modifications
* 	[**Single Result Dataset**](documentation/Simulation_Execution.md#4-execute-simulation--produce-system-event-dataset) 
as a 2 dimensional `list`
    * Returns a single dataset instead of multiple datasets per Monte Carlo simulation as in `0.3.1`:
        * New System Metrics as dataset attributes: 
            * **Simulation** (Alpha) is a unique identifier being developed to represent Experiments as stated above and 
            will be renamed accordingly
                * **Subset** is a unique identifier of Monte-Carlo simulations produced by parameter sweeps
    * Note: Returning a single dataset was originally specified during the project’s inception instead of multiple per 
    simulation

###### Examples:
* **ver. ≥ `0.4.22`:**
    ```python
    import pandas as pd
    from tabulate import tabulate
    from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
    import system_model_A, system_model_B
    from cadCAD import configs
  
    exec_mode = ExecutionMode()
    local_ctx = ExecutionContext(context=exec_mode.local_mode)
    simulation = Executor(exec_context=local_ctx, configs=configs)
    raw_result, sys_model, _ = simulation.execute()
  
    result = pd.DataFrame(raw_result)
    print(tabulate(result, headers='keys', tablefmt='psql'))
    ```
    Results:
    ```
    +----+------------+-----------+----+---------------------+------------+--------+-----+---------+----------+
    |    | s1         | s2        | s3 | timestamp           | simulation | subset | run | substep | timestep |
    |----+------------+-----------+----+---------------------+------------+--------+-----+---------+----------|
    |  0 | 0.0        | 0.0       |  1 | 2018-10-01 15:16:24 |          0 |      0 |   1 |       0 |        0 |
    |  1 | 1.0        | 4         |  5 | 2018-10-01 15:16:25 |          0 |      0 |   1 |       1 |        1 |
    |  2 | 2.0        | 6         |  5 | 2018-10-01 15:16:25 |          0 |      0 |   1 |       2 |        1 |
    |  3 | 3.0        | [ 30 300] |  5 | 2018-10-01 15:16:25 |          0 |      0 |   1 |       3 |        1 |
    |  4 | 0          | 0         |  1 | 2018-10-01 15:16:24 |          1 |      0 |   1 |       0 |        0 |
    |  5 | 1          | 0         |  5 | 2018-10-01 15:16:25 |          1 |      0 |   1 |       1 |        1 |
    |  6 | a          | 0         |  5 | 2018-10-01 15:16:25 |          1 |      0 |   1 |       2 |        1 |
    |  7 | ['c', 'd'] | [ 30 300] |  5 | 2018-10-01 15:16:25 |          1 |      0 |   1 |       3 |        1 |
    +----+------------+-----------+----+---------------------+------------+--------+-----+---------+----------+
    ```
* **ver. `0.3.1`:**
    ```python
    import pandas as pd
    from tabulate import tabulate
    from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
    import system_model_A, system_model_B
    from cadCAD import configs
    
    exec_mode = ExecutionMode()
    
    multi_ctx = ExecutionContext(context=exec_mode.multi_proc)
    simulation = Executor(exec_context=multi_ctx, configs=configs)
    
    i = 0
    config_names = ['sys_model_A', 'sys_model_B']
    for raw_result, _ in simulation.execute():
        result = pd.DataFrame(raw_result)
        print()
        print(f"{config_names[i]} Result: System Events DataFrame:")
        print(tabulate(result, headers='keys', tablefmt='psql'))
        print()
        i += 1
    ```
    Results:
    ```
    +----+------------+-----------+----+---------------------+-----+---------+----------+
    |    | s1         | s2        | s3 | timestamp           | run | substep | timestep |
    |----+------------+-----------+----+---------------------+-----+---------+----------|
    |  0 | 0.0        | 0.0       |  1 | 2018-10-01 15:16:24 |   1 |       0 |        0 |
    |  1 | 1.0        | 4         |  5 | 2018-10-01 15:16:25 |   1 |       1 |        1 |
    |  2 | 2.0        | 6         |  5 | 2018-10-01 15:16:25 |   1 |       2 |        1 |
    |  3 | 3.0        | [ 30 300] |  5 | 2018-10-01 15:16:25 |   1 |       3 |        1 |
    |  4 | 0          | 0         |  1 | 2018-10-01 15:16:24 |   1 |       0 |        0 |
    |  5 | 1          | 0         |  5 | 2018-10-01 15:16:25 |   1 |       1 |        1 |
    |  6 | a          | 0         |  5 | 2018-10-01 15:16:25 |   1 |       2 |        1 |
    |  7 | ['c', 'd'] | [ 30 300] |  5 | 2018-10-01 15:16:25 |   1 |       3 |        1 |
    +----+------------+-----------+----+---------------------+-----+---------+----------+
    ```
    
* **Flattened Configuration List:** The `cadCAD.configs` (System Model Configuration) `list` has been **temporarily** 
flattened to contain single run `cadCAD.configuration.Configuration` objects to both fault-tolerant simulation and 
elastic workloads. This functionality will be restored in a subsequent release by a class that returns 
`cadCAD.configs`'s original representation in ver. `0.3.1`.
    * The conversion utilities have been provided to restore its original representation of configurations with 
    runs >= 1
        * [System Configuration Conversions](documentation/System_Configuration.md)
            * Configuration as List of Configuration Objects (as in ver. `0.3.1`) 
            * New: System Configuration as a Pandas DataFrame
            * New: System Configuration as List of Dictionaries
            
###### Examples:
* Notes:
    * `configs` is temporarily returned in a flattened format and reformatted into its intended format 
    * `Configuration` objects at `0x10790e470` and `0x1143dd630` are reconstituted into objects at `0x10790e7b8` 
    and `0x116268908` respectively.
* **ver. ≥ `0.4.22`:** 
    ```python
    from pprint import pprint
    from documentation.examples import sys_model_A, sys_model_B
    from cadCAD.configuration.utils import configs_as_objs, configs_as_dataframe, configs_as_dicts
    from cadCAD import configs
    
    flattened_configs = configs
    
    print('Flattened Format: Temporary')  
    pprint(flattened_configs)
    print()
    
    print('Intended Format:')
    intended_configs = configs_as_objs(flattened_configs)
    pprint(intended_configs)
    print()
    ```
        
    Result:
    ```bash
    Flattened Format: Temporary
    [<cadCAD.configuration.Configuration object at 0x10790e470>,
     <cadCAD.configuration.Configuration object at 0x10790e7b8>,
     <cadCAD.configuration.Configuration object at 0x1143dd630>,
     <cadCAD.configuration.Configuration object at 0x116268908>]
    
    Intended Format:
    [<cadCAD.configuration.Configuration object at 0x10790e7b8>,
     <cadCAD.configuration.Configuration object at 0x116268908>]
    ```


##### Expandable state and policy update parameter space: 
* Enables the development of feature enhancements that involve the use of additional parameters without requiring users 
to modify their update parameters spaces when upgrading to newer versions. For this reason state / policy update 
examples in documentation include an additional `**kwargs` parameter.
    * [State Updates](documentation/README.md#state-update-functions)
    * [Policy Updates](documentation/README.md#state-update-functions)
    
###### Examples:
* **ver. ≥ `0.4.22`:**
    ```python
    def state_update(_params, substep, sH, s, _input, **kwargs):
        ...
        return 'state_variable_name', new_value

    def policy(_params, substep, sH, s, **kwargs):
        ...
        return {'signal_1': value_1, ..., 'signal_N': value_N}
    ```
* **ver. `0.3.1`:**

    ```python
    def state_update(_params, substep, sH, s, _input):
        ...
        return 'state_variable_name', new_value

    def policy(_params, substep, sH, s):
        ...
        return {'signal_1': value_1, ..., 'signal_N': value_N}
    ```


### May 29, 2020
* Packaging: Add [Nix](https://nixos.org/) derivation and shell for local development and distribution of cadCAD package 
using Nix. Nix is a powerful package manager for Linux and other Unix systems that makes package management reliable and 
reproducible, allowing you to share your development and build environments across different machines.
