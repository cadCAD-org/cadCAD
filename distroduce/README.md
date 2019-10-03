```
   ___   _      __        _  __         __           __
  / _ \ (_)___ / /_ ____ (_)/ /  __ __ / /_ ___  ___/ /
 / // // /(_-</ __// __// // _ \/ // // __// -_)/ _  / 
/____//_//___/\__//_/ _/_//_.__/\_,_/ \__/ \__/ \_,_/  
  / _ \ ____ ___  ___/ /__ __ ____ ___                 
 / ___// __// _ \/ _  // // // __// -_)                
/_/   /_/   \___/\_,_/ \_,_/ \__/ \__/                 
by Joshua E. Jodesty                                                       
                                       
```
## What?: *Description*
***Distributed Produce*** (**[distroduce](distroduce)**) is a message simulation and throughput benchmarking framework / 
cadCAD execution mode that leverages Apache Spark and Kafka Producer for optimizing Kafka cluster configurations and 
debugging real-time data transformations. *distroduce* leverages cadCAD's user-defined event simulation template and 
framework to simulate messages sent to Kafka clusters. This enables rapid and iterative design, debugging, and message 
publish benchmarking of Kafka clusters and real-time data processing using Kafka Streams and Spark (Structured) 
Streaming. 

##How?: *A Tail of Two Clusters*
***Distributed Produce*** is a Spark Application used as a cadCAD Execution Mode that distributes Kafka Producers, 
message simulation, and message publishing to worker nodes of an EMR cluster. Messages published from these workers are 
sent to Kafka topics on a Kafka cluster from a Spark bootstrapped EMR cluster.

##Why?: *Use Case*
* **IoT Event / Device Simulation:** Competes with *AWS IoT Device Simulator* and *Azure IoT Solution Acceleration: 
Device Simulation*. Unlike these products, *Distributed Produce* enables a user-defined state updates and agent actions, 
as well as message publish benchmarking
* **Development Environment for Real-Time Data Processing / Routing:**

##Get Started:

### 0. Set Up Local Development Environment: see [Kafka Quickstart](https://kafka.apache.org/quickstart)
**a.** Install `pyspark`
```bash
pip3 install pyspark
``` 
**b.** Install & Unzip Kafka, Create Kafka `test` topic, and Start Consumer
```bash
sh distroduce/configuration/launch_local_kafka.sh
```
**c.** Run Simulation locally
```bash
python3 distroduce/local_messaging_sim.py
```

### 1. Write cadCAD Simulation: 
* [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation)
* [Tutorials](https://github.com/BlockScience/cadCAD/tree/master/tutorials)

* **Terminology:**
    * ***Initial Conditions*** - State Variables and their initial values (Start event of Simulation)
    * ***[Policy Functions:](https://github.com/BlockScience/cadCAD/tree/master/documentation#Policy-Functions)*** - 
    computes one or more signals to be passed to State Update Functions
    * ***[State Update Functions]((https://github.com/BlockScience/cadCAD/tree/master/documentation#state-update-functions)):*** - 
    updates state variables change over time
    * ***[Partial State Update Block](https://github.com/BlockScience/cadCAD/tree/master/documentation#State-Variables) (PSUB):*** - 
    a set of State Update Functions and Policy Functions that update state records
    ![](https://i.imgur.com/9rlX9TG.png)


**Note:** State Update and Policy Functions now have the additional / undocumented parameter `kafkaConfig`

**a.** **Define Policy Functions:**
* [Example:](distroduce/action_policies.py) Two users interacting on separate chat clients and entering / exiting chat 

**b.** **Define State Update Functions:**
* [Example:](distroduce/state_updates.py) Used for logging and maintaining state of user actions defined by policies

**c.** **Define Initial Conditions & Partial State Update Block:**
* **Initial Conditions:** [Example](distroduce/messaging_sim.py)
* **Partial State Update Block (PSUB):** [Example](distroduce/simulation.py)

**d.** **Create Simulation Executor:** Used for running a simulation
* [Local](distroduce/local_messaging_sim.py)
* [EMR](distroduce/messaging_sim.py)

### 2. [Configure EMR Cluster](distroduce/configuration/cluster.py)

### 3. Launch EMR Cluster:
**Option A:** Preconfigured Launch
```bash
python3 distroduce/emr/launch.py
```
**Option B:** Custom Launch - [Example](distroduce/emr/launch.py)
```python
from distroduce.emr.launch import launch_cluster
from distroduce.configuration.cluster import ec2_attributes, bootstrap_actions, instance_groups, configurations
region = 'us-east-1'
cluster_name = 'distibuted_produce'
launch_cluster(cluster_name, region, ec2_attributes, bootstrap_actions, instance_groups, configurations)
```

### 4. Execute Benchmark(s):
* **Step 1:** ssh unto master node
* **Step 2:** Spark Submit
    ```
    PRIVATE_IP=`hostname -I | xargs`
    spark-submit --master yarn --py-files distroduce.zip messaging_sim.py $PRIVATE_IP
    ```
