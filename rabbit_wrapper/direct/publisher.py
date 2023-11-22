from ..basic.publisher import BasicMessagePublisher
from ..rabbit import Rabbit
from typing import Any

class Publisher(BasicMessagePublisher):
    def __init__(self, rabbit: Rabbit, queue: str):
        super().__init__(rabbit)
        self.queue_name = str(queue)
        self.rabbit.declare_queue(self.queue_name)
    
    def publish_message(self, body: Any):
        self.send_message(
            body=body,
            exchange_name='', # default exchange sends directly to queue
            routing_key=self.queue_name
        )