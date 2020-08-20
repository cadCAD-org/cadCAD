from datetime import datetime

# ToDo: Model Async communication here
# ToDo: Configuration of Input
def configure_producer(msg, config):
    from kafka import KafkaProducer
    def send_messages(events):
        producer = KafkaProducer(**config)

        start_timestamp = datetime.now()
        for event in range(events):
            producer.send('test', msg(event)).get()
        delta = datetime.now() - start_timestamp

        return start_timestamp, delta.total_seconds()

    return send_messages
