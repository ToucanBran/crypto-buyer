import pika
from contextlib import contextmanager
from pika.adapters.blocking_connection import BlockingChannel

@contextmanager
def queue(configs):
    rabbit = RabbitMqWrapper(configs)
    try:
        rabbit.open_channel(rabbit.get_connection_params())
        yield rabbit
    finally:
        if rabbit.channel_connected():
            rabbit.channel.close()


class RabbitMqWrapper:
    channel: BlockingChannel = None
    def __init__(self, configs):
        self.configs = configs

    def get_connection_params(self) -> BlockingChannel:
        if self.channel_connected():
            return self.channel
        credentials = pika.PlainCredentials(self.configs["user"], self.configs["password"])
        cp = pika.ConnectionParameters(port=self.configs["port"], host=self.configs["host"], virtual_host=self.configs["vhost"],
                                    credentials=credentials)
        
        return cp

    def open_channel(self, connection_params: pika.ConnectionParameters=None):
        if connection_params is None:
            connection_params = self.get_connection_params()
        connection = pika.BlockingConnection(connection_params)
        self.channel = connection.channel()
        self.channel.queue_declare(self.configs["name"], durable=True)
        return self.channel
    
    def push(self, message):
        if not self.channel_connected():
            raise Exception("Cannot push message, no rabbitmq connection.")
        self.channel.basic_publish(exchange='',
                    routing_key=self.configs["name"],
                    body=message)

    def start_consuming(self, callback):
        if not self.channel_connected():
            raise Exception("Cannot receive messages, no rabbitmq connection.")
        self.channel.basic_consume(queue=self.configs["name"], on_message_callback=callback, auto_ack=True)

        self.channel.start_consuming()

    def channel_connected(self) -> bool:
        return self.channel is not None and self.channel.is_open

    def close_connection(self):
        if self.channel_connected():
            self.channel.close()
