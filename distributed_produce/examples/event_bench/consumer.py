from kafka import KafkaConsumer
from datetime import datetime


consumer = KafkaConsumer('test', bootstrap_servers=['localhost:9092'])

i = 1
for message in consumer:
    percent = i / 10000
    print(str(datetime.now()) + " - " + str(percent) + ": " + str(i))
    i += 1
