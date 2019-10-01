#!/bin/bash
# SSH into all machines
ssh -i ~/.ssh/joshua-IAM-keypair.pem hadoop@
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install pathos kafka-python

# SetUp Window: head node
cd ~
#sudo python3 -m pip install --upgrade pip
#sudo python3 -m pip install pathos kafka-python
sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh
wget http://apache.spinellicreations.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -xzf kafka_2.12-2.3.0.tgz
cd kafka_2.12-2.3.0
bin/zookeeper-server-start.sh config/zookeeper.properties &
bin/kafka-server-start.sh config/server.properties &
# get ip
bin/kafka-topics.sh --create --bootstrap-server 10.0.0.9:9092 --replication-factor 1 --partitions 1 --topic test
# bin/kafka-topics.sh --list --bootstrap-server 10.0.0.9:9092

# Consume (Window): head node
kafka_2.12-2.3.0/bin/kafka-console-consumer.sh --bootstrap-server 10.0.0.9:9092 --topic test --from-beginning
# DELETE
# bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic test


# local
python3 setup.py sdist bdist_wheel
pip3 install dist/*.whl
# SCP: all nodes
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-18-206-12-181.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-34-239-171-181.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-3-230-154-170.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-18-232-52-219.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-34-231-70-210.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem dist/*.whl hadoop@ec2-34-231-243-101.compute-1.amazonaws.com:/home/hadoop/


sudo python3 -m pip install *.whl


# SCP head node
# ToDo: zip build for cadCAD OR give py library after whl install
scp -i ~/.ssh/joshua-IAM-keypair.pem distroduce/dist/distroduce.zip hadoop@ec2-18-206-12-181.compute-1.amazonaws.com:/home/hadoop/
scp -i ~/.ssh/joshua-IAM-keypair.pem distroduce/messaging_sim.py hadoop@ec2-18-206-12-181.compute-1.amazonaws.com:/home/hadoop/
#scp -i ~/.ssh/joshua-IAM-keypair.pem dist/distroduce.zip hadoop@ec2-18-232-54-233.compute-1.amazonaws.com:/home/hadoop/
#scp -i ~/.ssh/joshua-IAM-keypair.pem examples/event_bench/main.py hadoop@ec2-18-232-54-233.compute-1.amazonaws.com:/home/hadoop/


# Run Window: Head Node
spark-submit --master yarn messaging_app.py
# spark-submit --master yarn --py-files distroduce.zip main.py

# Cluster Config
#[
#  {
#    "Classification": "spark-env",
#    "Configurations": [
#        {
#            "Classification": "export",
#            "ConfigurationProperties": {
#                "PYSPARK_PYTHON": "/usr/bin/python3",
#                "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
#            }
#        }
#    ]
#  },
#  {
#    "Classification": "spark-defaults",
#    "ConfigurationProperties": {
#      "spark.sql.execution.arrow.enabled": "true"
#    }
#  },
#  {
#    "Classification": "spark",
#    "Properties": {
#      "maximizeResourceAllocation": "true"
#    }
#  }
#]

