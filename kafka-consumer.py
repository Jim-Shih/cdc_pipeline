from confluent_kafka import Consumer, KafkaException, KafkaError

consumer = Consumer(
    {
        "bootstrap.servers": "localhost:9092",
        "group.id": "mygroup",
        "auto.offset.reset": "earliest",
    }
)

consumer.subscribe(["my_connect_configs"])

try:
    while 1:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                raise KafkaException(msg.error())
        print(
            "%% %s [%d] at offset %d with key %s:\n"
            % (msg.topic(), msg.partition(), msg.offset(), str(msg.key()))
        )
        print(msg.value())

except KeyboardInterrupt:
    pass
