#!/bin/bash

scp -i ~/.ssh/joshua-IAM-keypair.pem ~/Projects/event-bench/event_bench.py \
hadoop@ec2-3-230-158-62.compute-1.amazonaws.com:/home/hadoop/

