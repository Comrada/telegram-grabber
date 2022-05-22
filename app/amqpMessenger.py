import json
from typing import List

from pika import BlockingConnection, URLParameters


class AmqpMessenger:

    def __init__(self, host, port, user, password, vhost):
        self.url = f"amqp://{user}:{password}@{host}:{port}{vhost}"
        self.connection = None
        self.channel = None

    def __del__(self):
        self.__close_connection()

    def __init_connection(self):
        parameters = URLParameters(self.url)
        self.connection = BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def __close_connection(self):
        if self.channel is not None and self.channel.is_open:
            self.channel.close()
        if self.connection is not None and self.connection.is_open:
            self.connection.close()

    def send_messages(self, exchange, routing_key, messages: List[dict]):
        event = self.__create_event(messages)
        self.__init_connection()
        self.channel.basic_publish(exchange=exchange,
                                   routing_key=routing_key,
                                   body=event)
        self.__close_connection()

    @staticmethod
    def __create_event(messages: List[dict]) -> bytes:
        return bytes(json.dumps(messages, default=str), 'utf-8')
