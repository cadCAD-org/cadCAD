#!/bin/bash
#spark-submit --master yarn event_bench.py
spark-submit --py-files dist/distroduce.zip examples/event_bench/main.py