# Defining connection
```python
from rabbit_wrapper import Rabbit, Consumer

# create a **blocking** connection to rabbitmq
rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True)
```

# Publishing messages
```python
# specify the queue you want to publish the messages to
publisher = Publisher(rabbit, 'my_queue')

message = {"some": "random message of any type. this one is a dictionary."}
publisher.publish_message(message)
```

# Consuming messages
```python
# specify the queue you want to listen to
consumer = Consumer(rabbit, 'my_queue')

def process_request(body):
    print(f'Processed message: {body}')

# start listening to messages coming to the queue,
# and handle them as they come in, using the `process_request` function
consumer.consume_messages(process_request)

# since the connection is blocking, no line after this will run.
# to make it non-blocking, set blocking=False when defining the Rabbit connection.

print("this line won't run")
```

Alternatively, if you want to get just one message at a time from the queue, do the following
```python
message = consumer.get_message()
```
