from src import Rabbit, TopicPublisher
import sys

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)

topic = sys.argv[1] if len(sys.argv) > 1 else "some.thing"
message = sys.argv[2] if len(sys.argv) > 2 else "hello world"
print(f"sending to topic: {topic} message: {message}")

publisher = TopicPublisher(rabbit, topic)


class Test:
    def __init__(self, message):
        self.message = message

publisher.publish_message(Test(message + " sent through class"))