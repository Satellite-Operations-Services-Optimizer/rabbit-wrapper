from src import Rabbit, Publisher

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)
foo_publisher = Publisher(rabbit, 'foo_queue')
bar_publisher = Publisher(rabbit, 'bar_queue')

foo_message = {"message": "i am foo"}
bar_message = {"message": "i am bar"}

class Test:
    def __init__(self, message):
        self.message = message

foo_publisher.publish_message(Test("foo msg"))
bar_publisher.publish_message("bar msg")