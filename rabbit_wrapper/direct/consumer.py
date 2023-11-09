import logging
from typing import Callable, Any
from ..rabbit import Rabbit
from ..basic.consumer import BasicMessageConsumer

logger = logging.getLogger(__name__)

class Consumer(BasicMessageConsumer):
    def __init__(self, rabbit: Rabbit, queue_name: str):
        super().__init__(rabbit)
        self.queue_name = str(queue_name)
        self.rabbit.declare_queue(self.queue_name)
    
    def get_message(self, auto_ack: bool = False):
        (_, _, body) = super().get_message(self.queue_name, auto_ack)
        body = self.decode_message(body)
        return body
    
    def consume_messages(self, callback: Callable[[Any], Any]):
        logged_callback = self._logged_message_callback(callback)
        super().consume_messages(self.queue_name, logged_callback)
    
    def _logged_message_callback(self, callback: Callable[[Any], Any]):
        def callback_wrapper(channel, method, properties, body):
            logger.debug(f"Message consumed from queue {self.queue_name}. Message body: {body}")
            body = self.decode_message(body)
            callback(body)
        return callback_wrapper
        