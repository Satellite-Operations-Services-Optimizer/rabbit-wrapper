from src import Rabbit, TopicConsumer
import sys

def process_request(body):
    print(f'Processed message: {body}')

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)

"""accept system argument for topic"""
topic = sys.argv[1] if len(sys.argv) > 1 else "some.thing"

consumer = TopicConsumer(rabbit, topic)
consumer.register_callback(process_request)
print(f"consumer listening to topic: {topic}")
rabbit.channel.start_consuming()