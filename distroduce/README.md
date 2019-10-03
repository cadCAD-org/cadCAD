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

##Description:
***Distributed Produce*** (**[distroduce](distroduce)**) is a message simulation and throughput benchmarking framework / 
cadCAD execution mode that leverages Apache Spark and Kafka Producer for optimizing Kafka cluster configurations and 
debugging real-time data transformations (i.e. Kafka Streams, Spark (Structured) Streaming). cadCAD's user-defined event 
simulation framework is used to simulate messages sent to Kafka clusters.

##Use Cases:
* **Education:** I wanted to provide a tool for Insight Data Engineering Fellows implementing real-time data processing 
that enables rapid and iterative design, debugging, and message publish benchmarking of Kafka clusters and real-time 
data processing using Kafka Streams and Spark (Structured) Streaming.
* **IoT:** Competes with *AWS IoT Device Simulator* and *Azure IoT Solution Acceleration: Device Simulation*. Unlike 
these products, *Distributed Produce* enables a user-defined state updates and agent actions, as well as message publish 
benchmarking

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

### 1. Write Simulation: 
* [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation)
* [Tutorials](https://github.com/BlockScience/cadCAD/tree/master/tutorials)

**Note:** State Update and Policy Functions now have the additional / undocumented parameter `kafkaConfig`

**a.** **Define Policy Functions:** Two users interacting on separate chat clients and entering / exiting chat rooms 
* [Example](distroduce/action_policies.py)
* [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation#Policy-Functions)

**b.** **Define State Update Functions:** Used for logging and maintaining state of user actions defined by policies
* [Example](distroduce/state_updates.py)
* [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation#state-update-functions)

**c.** **Define Initial Conditions & Partial State Update Block**
* **Initial Conditions** - State Variables and their initial values
    * [Example](distroduce/messaging_sim.py)
    * [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation#State-Variables)

* **Partial State Update Block (PSUB)** - a set of State Update Functions and Policy Functions that update state records
    * [Example](distroduce/simulation.py)
    * [Documentation](https://github.com/BlockScience/cadCAD/tree/master/documentation#Partial-State-Update-Blocks)
    ![](https://i.imgur.com/9rlX9TG.png)

**d.** **Create Simulation Executor:** Used for running a simulation
* [Local](distroduce/local_messaging_sim.py)
* [EMR](distroduce/messaging_sim.py)

### 2. [Configure EMR Cluster](distroduce/configuration/cluster.py)

### 3. Launch EMR Cluster:
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
