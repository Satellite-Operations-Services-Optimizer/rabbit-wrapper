import pika
from pika.exceptions import AMQPConnectionError
import ssl
import time
from abc import abstractmethod

class Connection:
    connection = None
    def __init__(self, user: str, password: str, host: str, port: int, vhost='/', protocol="amqp"):
        credentials = pika.PlainCredentials(str(user), str(password))
        self.parameters = pika.ConnectionParameters(
            host=str(host),
            port=int(port),
            virtual_host=str(vhost),
            credentials=credentials,
            heartbeat=36000,
            connection_attempts=5
        )
        if protocol == "amqps":
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")
            self.parameters.ssl_options = pika.SSLOptions(context=ssl_context)
    
    def check_connection(self):
        if not self.connection or self.connection.is_closed:
            return self.connect()
        return self.connection

    def connect(self):
        tries = 0
        while True:
            try:
                self.connection = self._create_pika_connection()
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    break
            except (AMQPConnectionError, Exception) as e:
                print(e)
                time.sleep(5)
                tries += 1
                if tries == 20:
                    raise AMQPConnectionError(e)
        return self.connection
    
    def close(self):
        self.channel.close()
        self.connection.close()

    @abstractmethod
    def _create_pika_connection(self):
        raise NotImplementedError()



class BlockingConnection(Connection):
    def _create_pika_connection(self):
        return pika.BlockingConnection(self.parameters)

class SelectConnection(Connection):
    def _create_pika_connection(self):
        pika_connection = pika.SelectConnection(self.parameters)
        pika_connection.ioloop.start()
        return pika_connection

    def close(self):
        super().close()
        self.connection.ioloop.start()
