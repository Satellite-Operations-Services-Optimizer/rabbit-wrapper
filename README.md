This is just like a regular pip package. No need for you to pip install it though. I have included it in the requirements.txt file, so it will be installed along with all the other dependencies. All you need to do is just import it into your python file.

# Defining connection
```python
from rabbit_wrapper import Rabbit, Publisher, Consumer, TopicPublisher, TopicConsumer

# create a **blocking** connection to rabbitmq
rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)
```

# Direct Messaging
## Publishing messages
```python
# specify the queue you want to publish the messages to
publisher = Publisher(rabbit, 'my_queue')

message = {"some": "random message of any type. this one is a dictionary."}
publisher.publish_message(message)
```

## Consuming messages
```python
# specify the queue you want to listen to
consumer = Consumer(rabbit, 'my_queue')

def process_request(body):
    print(f'Processed message: {body}')

# start listening to messages coming to the queue,
# and handle them as they come in, using the `process_request` function
consumer.register_callback(process_request)

# start consuming messages. since the connection is blocking, no line after this will run.
rabbit.start_consuming()

print("this line won't run")
```

Alternatively, if you want to get just one message at a time from the queue, do the following
```python
message = consumer.get_message()
```

# Topic Messaging
## Publishing messages
```python
# specify the topic you want to publish the messages to
publisher = Publisher(rabbit, 'order.image.created')

message = {"image_id": 1, "resolution": "high}
publisher.publish_message(message)
```

## Consuming messages
```python
# Create your consumer
consumer = TopicConsumer(rabbit)

# bind it to the topics you want the consumer to listen to. You can pass a topic, or a list of topics, that you want this consumer to listen to
consumer.bind("order.*.created")

def process_request(body):
    print(f'Processed message: {body}')

# start listening to messages coming to the topics you've binded to,
# and handle them as they come in, using the `process_request` function
consumer.register_callback(process_request)

# start consuming messages. since the connection is blocking, no line after this will run.
rabbit.start_consuming()

print("this line won't run")
```
