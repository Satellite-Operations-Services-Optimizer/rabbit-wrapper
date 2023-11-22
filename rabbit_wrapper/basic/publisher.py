import pika
import json
import logging
import msgpack
from ..rabbit import Rabbit

logger = logging.getLogger(__name__)

class BasicMessagePublisher:
    def __init__(self, rabbit: Rabbit):
        self.rabbit = rabbit
        self.channel = rabbit.channel
        self.channel_tag = None

    def send_message(
        self,
        exchange_name: str,
        routing_key: str,
        body: any,
    ):
        self.rabbit.check_connection()
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=self.encode_message(body),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        logger.debug(
            f"Sent message. Exchange: {exchange_name}, Routing Key: {routing_key}, Body: {body}"
        )

    def encode_message(self, body: dict, encoding_type: str = "bytes"):
        if encoding_type == "bytes":
            return msgpack.packb(body)
        else:
            raise NotImplementedError
