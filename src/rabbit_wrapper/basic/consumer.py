import logging
import json
import msgpack
from ..rabbit import Rabbit

logger = logging.getLogger(__name__)

class BasicMessageConsumer:
    def __init__(self, rabbit: Rabbit):
        self.rabbit = rabbit
        self.channel = rabbit.channel
        self.channel_tag = None

    def get_message(self, queue_name: str, auto_ack: bool = False):
        logger.debug(f"Getting message from queue {queue_name}")
        method_frame, header_frame, body = self.channel.basic_get(
            queue=queue_name, auto_ack=auto_ack
        )
        if method_frame:
            logger.debug(f"{method_frame}, {header_frame}, {body}")
            return method_frame, header_frame, body
        else:
            logger.debug("No message returned")
            return None

    def register_callback(self, queue, callback):
        self.rabbit.ensure_connected()
        self.channel_tag = self.channel.basic_consume(
            queue=queue, on_message_callback=callback, auto_ack=True
        )
        logger.debug(f" [*] Waiting for messages from queue {queue}. To exit press CTRL+C")
        self.channel.basic_qos(prefetch_count=1)
    
    def cancel_callbacks(self):
        if self.channel_tag is not None:
            self.channel.basic_cancel(self.channel_tag)
            self.channel_tag = None
        else:
            logger.error("Do not cancel a non-existing job")

    def decode_message(self, body):
        if type(body) is bytes:
            message = json.loads(msgpack.unpackb(body))
            return message["body"] # encoder wraps message in json with key "body" (to prevent errors when decoding non-json messages)
        else:
            raise NotImplementedError