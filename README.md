# Defining connection
```python
from rabbit_wrapper import Rabbit, Consumer

rabbit = Rabbit('localhost', 5672, 'guest', 'guest', '/', blocking=True) # note, blocking=True means this is a blocking connection
```

# Publishing messages
```python
publisher = Publisher(rabbit, 'my_queue') # specify the queue you want to publish the messages to

message = {"some": "random message of any type. this one is a dictionary."}
publisher.publish_message(message)
```

# Consuming messages
```python
consumer = Consumer(rabbit, 'my_queue') # specify the queue you want to listen to

def process_request(body):
    print(f'Processed message: {body}')

# start listening to messages coming to the queue, and handle them as they come in
consumer.consume_messages(process_request)
print("this line won't run") # since the connection is blocking, This line won't run. It is blocked, only passing messages it receives to the `process_request` handler. Set blocking=False to prevent this

```
Alternatively, if you want to get just one message at a time from the queue, do the following
```python
message = consumer.get_message()
```
