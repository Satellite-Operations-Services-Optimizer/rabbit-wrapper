from src.rabbit_wrapper import Rabbit, Publisher

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)
publisher = Publisher(rabbit, 'my_queue')

message = {"message_details": "some message details"}
publisher.publish_message(message)