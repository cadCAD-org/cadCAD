#!/bin/bash
wget http://apache.spinellicreations.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -xzf kafka_2.12-2.3.0.tgz
cd kafka_2.12-2.3.0
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test --from-beginning
