import logging
from typing import Callable, Any, Optional
from ..rabbit import Rabbit
from ..basic.consumer import BasicMessageConsumer

logger = logging.getLogger(__name__)

class Consumer(BasicMessageConsumer):
    def __init__(self, rabbit: Rabbit, queue: Optional[str]):
        super().__init__(rabbit)
        if queue is not None:
            self.queue_name = str(queue)
            self.rabbit.declare_queue(self.queue_name)
        else:
            result = self.rabbit.declare_queue('') # create new queue
            self.queue_name = result.method.queue
    
    def get_message(self, auto_ack: bool = False):
        (_, _, body) = super().get_message(self.queue_name, auto_ack)
        body = self.decode_message(body)
        return body
    
    def register_callback(self, callback: Callable[[Any], Any]):
        logged_callback = self._logged_message_callback(callback)
        super().register_callback(self.queue_name, logged_callback)
    
    def _logged_message_callback(self, callback: Callable[[Any], Any]):
        def callback_wrapper(channel, method, properties, body):
            logger.debug(f"Message consumed from queue {self.queue_name}. Message body: {body}")
            body = self.decode_message(body)
            callback(body)
        return callback_wrapper
        