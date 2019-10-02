#!/bin/bash
sudo sed -i -e '$a\export PYSPARK_PYTHON=/usr/bin/python3' /etc/spark/conf/spark-env.sh
spark-submit --master yarn --py-files distroduce.zip messaging_sim.py $PRIVATE_IP