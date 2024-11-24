import logging
from datetime import datetime
from confluent_kafka import Producer
import json


class KafkaLogHandler(logging.Handler):
    def __init__(self, kafka_server: str, topic: str):
        super().__init__()
        self.producer = Producer({'bootstrap.servers': kafka_server,
                                  'linger.ms': 100,
                                  'batch.size': 65536,
                                  'acks': 'all'
                                  })
        self.topic = topic

    def stop(self):
        self.producer.flush()

    def emit(self, record):
        data = {
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            "datetime": str(datetime.fromtimestamp(record.created)),
        }
        if record.args:
            data["args"] = record.args

        message = json.dumps(data).encode('utf-8')

        def delivery_report(err, msg):
            """ Called once for each message produced to indicate delivery result.
                Triggered by poll() or flush(). """
            if err is not None:
                print('Message delivery failed: {}'.format(err))
            else:
                print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

        self.producer.produce(self.topic, message, callback=delivery_report)
