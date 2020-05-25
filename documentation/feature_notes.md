# Features Notes:
### May 18, 2020

#### [Distributed Execution Mode](https://github.com/BlockScience/distroduce/blob/master/documentation/dist_exec_doc.ipynb)
* Distributes simulations on horizontally scalable computing cluster to concurrently execute Monte-Carlo runs with 
Apache Spark on AWS EMR.
* Runs are executed via a DAG scheduler that parrelizes runs within cluster executors (“virtual threads”) across 
    multiple EC2 instances
    
#### [Local Execution Mode](documentation/Simulation_Execution.md)
* Default parallelization of Monte-Carlo simulations
* **Backwards Compatible** with given legacy modes names

#### [cadCAD Post-Processing Enhancements](https://github.com/BlockScience/distroduce/blob/master/documentation/dist_exec_doc.ipynb)
* Returns single dataset as three types depending on execution mode:
    * Distributed Mode: 
        * Spark RDD: 
            * Conversion Functions: 
                * Spark DataFrame
                    * SQL (Spark SQL / ANSI 2011)
                * Pandas DataFrame
            * Note: Conversion to DataFrames above
    * Local Mode: 
        * 2d List
* Changes:
    * Returning a single dataset was originally specified at the project’s inception instead of multiple per simulation
    * Two additional return types (Spark RDD & DataFrame)
* [System Configurations](https://github.com/BlockScience/distroduce/blob/master/documentation/dist_exec_doc.ipynb) return as 3 types 
    * System Configuration Dictionary List 
    * System Configuration DataFrame 
    * System Configuration Object List
        
#### [Auto-generate schema](https://github.com/BlockScience/distroduce/blob/master/documentation/dist_exec_doc.ipynb) from Initial Conditions to be applied to Spark DataFrames 

#### Backwards compatibility:
* Expandable state and policy update parameter space enables changes to the parameter space of updates while 
supporting backwards compatibility
* Legacy execution modes supported

#### Bug Fixes:
* [CTTF-462](https://blockscience.atlassian.net/browse/CTTF-462): single_proc & Multi_proc simulations stalls within the same module