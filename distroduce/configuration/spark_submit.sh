#!/bin/bash
PRIVATE_IP=`hostname -I | xargs`
spark-submit --master yarn --py-files distroduce.zip messaging_sim.py $PRIVATE_IP