# Changelog:

### August 5, 2020
##### [Experiments](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/README.md#introduction)
* `cadCAD.configuration.Experiment` (Alpha) is in development and needed to be released to support the implementation of 
web applications and proprietary feature extensions. It is intended to represent a unique identifier of an experiment of 
one or more configured System Models. For this reason, `append_configs` is a method of 
`cadCAD.configuration.Experiment`. As of now it does not support multi - system model simulation because configurations 
are still appended globally despite `append_config` being a method of Experiment.

* Examples:
    * **ver. `0.4.22`:**
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
##### [Local Execution Mode (Default)](documentation/Simulation_Execution.md)
* Local Execution Mode (Default): Implicit parallelization of Monte-Carlo / Stochastic simulations (Automatically 
selects Multi-Process / Threaded Mode if simulations are configure for a single run)
    * **Backwards Compatibility:** `cadCAD.engine.ExecutionMode` accepts legacy execution modes from ver. `0.3.1`
* Examples:
    * **ver. `0.4.22`:**
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
* 	[**Single Result Dataset**]((https://github.com/cadCAD-org/cadCAD/blob/master/documentation/Simulation_Execution.md#4-execute-simulation--produce-system-event-dataset)) as a 2 dimensional `list`
    * Returns a single dataset instead of multiple datasets per Monte Carlo simulation as in `0.3.1`:
        * New System Metrics as dataset attributes: 
            * **Simulation** (Alpha) is a unique identifier being developed to represent Experiments as stated above and 
            will be renamed accordingly
                * **Subset** is a unique identifier of Monte Carlo simulations produced by parameter sweeps
    * Note: Returning a single dataset was originally specified during the project’s inception instead of multiple per 
    simulation
    * Examples:
        * **ver. `0.4.22`:**
            ```python
            import pandas as pd
            from tabulate import tabulate
            from cadCAD import configs
            from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
          
            exec_mode = ExecutionMode()
            local_ctx = ExecutionContext(context=exec_mode.local_mode)
            simulation = Executor(exec_context=local_ctx, configs=configs)
            raw_result, sys_model, _ = simulation.execute()
          
            result = pd.DataFrame(raw_result)
            print(tabulate(result, headers='keys', tablefmt='psql'))
            ```
            Results:
            ```bash
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
            ```
    
* 	The `configs` `list` has been temporarily flattened to contain single run System Model `Configuration` objects to 
support elastic workloads. This functionality will be restored in a subsequent release by a class that returns 
`configs`'s original representation in ver. `0.3.1`.
    * The conversion utilities have been provided to restore its original representation of configurations with 
    runs >= 1
        * [System Configuration Conversions](documentation/System_Configuration.md)
            * Configuration as List of Configuration Objects (as in ver. `0.3.1`) 
            * New: System Configuration as a Pandas DataFrame
            * New: System Configuration as List of Dictionaries


##### Expandable state and policy update parameter space: 
* Enables the development of feature enhancements that involve the use of additional parameters without requiring users 
to modify their update parameters spaces when upgrading to newer versions. For this reason state / policy update 
examples in documentation include an additional `**kwargs` parameter.
    * [State Updates:](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/README.md#state-update-functions)
    * [Policy Updates:](https://github.com/cadCAD-org/cadCAD/blob/master/documentation/README.md#state-update-functions)


### May 29, 2020
* Packaging: Add [Nix](https://nixos.org/) derivation and shell for local development and distribution of cadCAD package 
using Nix. Nix is a powerful package manager for Linux and other Unix systems that makes package management reliable and 
reproducible, allowing you to share your development and build environments across different machines.
