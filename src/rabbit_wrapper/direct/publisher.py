from ..basic.publisher import BasicMessagePublisher

class Publisher(BasicMessagePublisher):
    def __init__(self, rabbit, queue_name):
        super().__init__(rabbit)
        self.queue_name = str(queue_name)
    
    def publish_message(self, body):
        self.send_message(
            body=body,
            exchange_name='', # default exchange sends directly to queue
            routing_key=self.queue_name
        )