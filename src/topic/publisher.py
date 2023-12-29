from ..basic.publisher import BasicMessagePublisher
from typing import Optional, Any
from ..rabbit import Rabbit

class TopicPublisher(BasicMessagePublisher):
    def __init__(self, rabbit: Rabbit, topic: str, exchange: str = 'default_topic_exchange'):
        super().__init__(rabbit)
        self.topic = str(topic)
        self.exchange_name = str(exchange)
        self.rabbit.declare_exchange(exchange_name=self.exchange_name, exchange_type='topic')
    
    def publish_message(self, body: Any):
        self.send_message(
            body=body,
            exchange_name=self.exchange_name,
            routing_key=self.topic
        )