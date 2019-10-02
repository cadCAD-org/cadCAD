#!/bin/bash
cd ~
yes | sudo python3 -m pip install --upgrade pip
yes | sudo python3 -m pip install pathos kafka-python
wget https://raw.githubusercontent.com/JEJodesty/cadCAD/dev/dist/cadCAD-0.0.2-py3-none-any.whl
yes | sudo python3 -m pip install cadCAD-0.0.2-py3-none-any.whl


# check for master node
PRIVATE_IP=localhost
IS_MASTER=false
if grep -i isMaster /mnt/var/lib/info/instance.json | grep -i true;
then
  IS_MASTER=true
  wget https://raw.githubusercontent.com/JEJodesty/cadCAD/dev/distroduce/dist/distroduce.zip
  wget https://raw.githubusercontent.com/JEJodesty/cadCAD/dev/distroduce/messaging_sim.py
  sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh
  wget http://apache.spinellicreations.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz
  tar -xzf kafka_2.12-2.3.0.tgz
  cd kafka_2.12-2.3.0
  bin/zookeeper-server-start.sh config/zookeeper.properties &
  bin/kafka-server-start.sh config/server.properties &
  bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic test
#  PRIVATE_IP=`hostname -I | xargs`
#  bin/kafka-topics.sh --create --bootstrap-server ${PRIVATE_IP}:9092 --replication-factor 1 --partitions 1 --topic test
fi
