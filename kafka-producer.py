from confluent_kafka import Producer, KafkaException, KafkaError

producer = Producer(
    {
        "bootstrap.servers": "localhost:9092",
        "queue.buffering.max.messages": 500000,
        "queue.buffering.max.ms": 1000,
    }
)

topic = "my_connect_configs"
msg = "Hello from Kafka Producer"

try:
    producer.produce(topic, value=msg)
    producer.flush()
    print("Message sent successfully")
except KafkaException as e:
    print(e)
except KeyboardInterrupt:
    pass
