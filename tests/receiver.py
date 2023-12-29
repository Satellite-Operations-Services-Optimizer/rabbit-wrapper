from src import Rabbit, Consumer

def process_request(body):
    print(f'Processed message: {body}')

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)

foo_consumer = Consumer(rabbit, 'foo_queue')
bar_consumer = Consumer(rabbit, 'bar_queue')

foo_consumer.register_callback(process_request)
print("foo consumer created!")
bar_consumer.register_callback(process_request)
print("bar consumer created!")
rabbit.channel.start_consuming()
print("done")