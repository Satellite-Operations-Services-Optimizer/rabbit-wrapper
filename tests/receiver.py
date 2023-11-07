from src.rabbit_wrapper import Rabbit, Consumer

def process_request(body):
    print(f'Processed message: {body}')

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)

consumer = Consumer(rabbit, 'my_queue')
consumer.consume_messages(process_request)