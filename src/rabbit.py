import logging
from .connection import SyncConnection, AsyncConnection

logger = logging.getLogger(__name__)
class Rabbit:
    def __init__(self, host: str, port: int, user: str, password: str, vhost: str ='/', blocking=False):
        if blocking:
            self.connection = SyncConnection(user, password, host, port, vhost)
        else:
            self.connection = AsyncConnection(user, password, host, port, vhost)
        self.connection.connect()
        self.channel = self.connection.channel
    
    def start_consuming(self):
        self.channel.start_consuming()
    
    def as_uri(self):
        return self.connection.as_uri()

    def declare_queue(
        self, queue_name, exclusive: bool = False
    ):
        self.ensure_connected()
        logger.debug(f"Trying to declare queue({queue_name})...")
        return self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive,
            durable=True
        )

    def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
        self.ensure_connected()
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )

    def bind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.ensure_connected()
        self.channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )

    def unbind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.channel.queue_unbind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )
    
    def ensure_connected(self):
        return self.connection.ensure_connected()

    def close(self):
        self.connection.close()
