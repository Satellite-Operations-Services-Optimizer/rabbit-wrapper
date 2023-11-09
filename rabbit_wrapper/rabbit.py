import logging
from .connection import BlockingConnection, SelectConnection

logger = logging.getLogger(__name__)
class Rabbit:
    def __init__(self, host: str, port: int, user: str, password: str, vhost: str ='/', blocking=False):
        if blocking:
            self.connection = BlockingConnection(user, password, host, port, vhost)
        else:
            self.connection = SelectConnection(user, password, host, port, vhost)
        self.connection.connect()
        self.channel = self.connection.channel

    def declare_queue(
        self, queue_name, exclusive: bool = False
    ):
        self.check_connection()
        logger.debug(f"Trying to declare queue({queue_name})...")
        self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive,
            durable=True
        )

    def declare_exchange(self, exchange_name: str, exchange_type: str = "direct"):
        self.check_connection()
        self.channel.exchange_declare(
            exchange=exchange_name, exchange_type=exchange_type
        )

    def bind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.check_connection()
        self.channel.queue_bind(
            exchange=exchange_name, queue=queue_name, routing_key=routing_key
        )

    def unbind_queue(self, exchange_name: str, queue_name: str, routing_key: str):
        self.channel.queue_unbind(
            queue=queue_name, exchange=exchange_name, routing_key=routing_key
        )
    
    def check_connection(self):
        return self.connection.check_connection()

    def close(self):
        self.connection.close()
