import logging
from typing import Callable, Any, Optional
from ..rabbit import Rabbit
from ..basic.consumer import BasicMessageConsumer

logger = logging.getLogger(__name__)

class TopicConsumer(BasicMessageConsumer):
    def __init__(self, rabbit: Rabbit, topic_selector: str, queue: Optional[str], exchange: Optional[str]):
        super().__init__(rabbit)
        self.binding_key = str(topic_selector)
        if queue is not None:
            self.queue_name = str(queue)
            self.rabbit.declare_queue(self.queue_name)
        else:
            result = self.rabbit.declare_queue('') # create new queue
            self.queue_name = result.method.queue

        if exchange is not None:
            self.exchange_name = str(exchange)
        else:
            self.exchange_name = 'default_topic_exchange'

        self.rabbit.declare_exchange(exchange_name=self.exchange_name, exchange_type='topic')
        self.rabbit.bind_queue(
            exchange_name=self.exchange_name,
            queue_name=self.queue_name,
            routing_key=self.binding_key
        )
    
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
        