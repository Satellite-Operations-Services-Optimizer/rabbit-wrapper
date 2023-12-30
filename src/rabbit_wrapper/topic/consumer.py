import logging
from typing import Callable, Any, Optional
from ..rabbit import Rabbit
from ..basic.consumer import BasicMessageConsumer

logger = logging.getLogger(__name__)

class TopicConsumer(BasicMessageConsumer):
    topics: set[str] = set()
    def __init__(self, rabbit: Rabbit, topic_selector: Optional[str], queue: str = "", exchange: str = 'default_topic_exchange', exclusive:bool=False):
        super().__init__(rabbit)

        if queue=="":
            result = self.rabbit.declare_queue('', exclusive=True) # delete queue when consumer disconnects (we won't be able to get the auto-generated name of the queue anyways, so might as well delete it)
            self.queue_name = result.method.queue
        else:
            self.queue_name = str(queue)
            self.rabbit.declare_queue(self.queue_name)

        self.exchange_name = str(exchange)
        self.rabbit.declare_exchange(exchange_name=self.exchange_name, exchange_type='topic')

        if topic_selector is not None:
            self.bind(str(topic_selector))
    
    def bind(self, topic: str|list[str]):
        if type(topic)!=list:
            topics = [topic]
        else:
            topics = topic
        
        for topic in topics:
            if topic in self.topics: continue
            self.topics.add(topic)
            self.rabbit.bind_queue(
                exchange_name=self.exchange_name,
                queue_name=self.queue_name,
                routing_key=topic
            )
        return self

    def unbind(self, topic: str):
        self.topics.remove(topic)
        self.rabbit.unbind_queue(
            exchange_name=self.exchange_name,
            queue_name=self.queue_name,
            routing_key=topic
        )
    
    def get_message(self, auto_ack: bool = False):
        (_, _, body) = super().get_message(self.queue_name, auto_ack)
        if body is not None:
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
        