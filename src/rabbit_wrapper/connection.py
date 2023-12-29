import pika
from pika.exceptions import AMQPConnectionError
import ssl
import time
from abc import abstractmethod
import logging
from typing import Optional
from pika.adapters.asyncio_connection import AsyncioConnection
from pika import SelectConnection
from threading import Thread

logger = logging.getLogger(__name__)
class Connection:
    connection: Optional[pika.BlockingConnection|AsyncioConnection] = None
    channel: Optional[pika.channel.Channel] = None
    def __init__(self, user: str, password: str, host: str, port: int, vhost='/', protocol="amqp"):
        self.credentials = pika.PlainCredentials(str(user), str(password))
        self.parameters = pika.ConnectionParameters(
            host=str(host),
            port=int(port),
            virtual_host=str(vhost),
            credentials=self.credentials,
            heartbeat=36000,
            connection_attempts=5
        )
        self.protocol = protocol
        if self.protocol == "amqps":
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")
            self.parameters.ssl_options = pika.SSLOptions(context=ssl_context)
    
    def as_uri(self):
        return f"{self.protocol}://{self.credentials.user}:{self.credentials.password}@{self.parameters.host}:{self.parameters.port}/{self.parameters.virtual_host}"
    
    def is_connected(self):
        return self.connection is not None and self.connection.is_open
    
    def ensure_connected(self):
        if not self.connection or self.connection.is_closed:
            return self.connect()
        return self.connection

    _is_connecting = False # Flag to track async connection status. True while trying to connect, False when succeeded/done trying.
    def connect(self):
        if self.is_connected(): return
        self._is_connecting = True
        self._start_connection()
        self._is_connecting = False
    
    reconnect_tries = 0
    max_reconnect_tries = 20
    reconnect_timeout = 5
    def _on_connection_error(self, connection, exception):
        logger.warning("RabbitMQ connection open failed. Retrying...")
        if self.reconnect_tries < self.max_reconnect_tries:
            time.sleep(self.reconnect_timeout)
            self.reconnect_tries += 1
            self.connect()
        else:
            self._is_connecting = False
            self.reconnect_tries = 0
            logger.exception(f"RabbitMQ connection could not be established after {self.reconnect_tries} tries. Error: {exception}")
            raise AMQPConnectionError(exception)
    
    @abstractmethod
    def _start_connection(self):
        raise NotImplementedError()

    
    @abstractmethod
    def close(self):
        raise NotImplementedError()


class SyncConnection(Connection):
    def _start_connection(self):
        logger.debug("RabbitMQ attempting to open connection...")
        try:
            self.connection = pika.BlockingConnection(self.parameters)
            self.channel = self.connection.channel()
            logger.debug("RabbitMQ connection opened successfully.")
        except (AMQPConnectionError, Exception) as e:
            self._on_connection_error(self.connection, e)
    
    def close(self):
        if self.channel is not None:
            self.channel.close()
            self.channel = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None

class AsyncConnection(Connection):
    def _start_connection(self):
        logger.debug("RabbitMQ attempting to open connection...")
        self.connection = SelectConnection(
            self.parameters,
            on_open_callback=self._on_connection_open,
            on_open_error_callback=self._on_connection_error,
            on_close_callback=lambda _: self.close(),
        )
        self._start_thread()
        # block until we are done trying to connect (until either we connected or there was an error)
        while self._is_connecting:
            pass

    def close(self):
        self._consuming = False
        if self.connection.is_closing or self.connection.is_closed:
            logger.info('Connection is closing or already closed')
        else:
            logger.info('Closing connection')
            self.connection.ioloop.stop()
            self.connection.close()

        if self.channel is not None:
            self.channel.close()
        if self.connection is not None:
            self.connection.close()
            self._start_thread()

    def _on_connection_open(self, connection):
        logger.debug("RabbitMQ connection opened successfully.")
        self.connection = connection
        self.connection.channel(on_open_callback=self._on_channel_open)
    
    def _on_channel_open(self, channel):
        self.channel = channel
        self._is_connecting = False # end of callback chain, we are done trying to connect
    
    io_thread: Optional[Thread] = None
    def _start_thread(self):
        self.io_thread = Thread(target=self.connection.ioloop.start)
        self.io_thread.start()