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

**Description:**
Distributed Produce (**distroduce**) is a cadCAD feature leveraging Apache Spark and Apache Kafka to enable in-stream 
data processing application development and throughput benchmarking for Kafka clusters. 

**Properties:**
* enables cadCAD's user-defined simulation framework to publish events/messages to Kafka Clusters
* enables scalable message publishing Kafka clusters by distributing simulated event/message creation and publishing on
an EMR cluster using Spark and Kafka Producer


#### Installation / Build From Source:
```
pip3 install -r requirements.txt
zip -rq distributed_produce/dist/distroduce.zip cadCAD/distroduce/
```

#### Usage:
```
spark-submit --py-files distributed_produce/dist/distroduce.zip distributed_produce/examples/event_bench/main.py
```
