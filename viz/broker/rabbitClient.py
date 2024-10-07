import pika
import time
import sys
import traceback

from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Creates a rabbitmq client.

This function creates a rabbitmq client using the provided configuration.
It tries to connect to the rabbitmq server and returns a channel.
If the connection fails, it retries every 1 second until a successful connection is made.

Parameters:
    conf (Conf): Configuration object containing rabbitmq connection details.

Returns:
    channel: A rabbitmq channel object.
"""


class RabbitMQClientConf(BaseSettings):
    rabbitmq_host: str
    rabbitmq_port: int = 5672
    rabbitmq_username: str
    rabbitmq_password: str

    model_config = SettingsConfigDict(env_prefix="CONF_")


class RabbitMQClient:
    def __init__(
        self, connection: pika.BlockingConnection, channel: pika.channel.Channel
    ):
        self.connection = connection
        self.channel = channel


def create_rabbitmq_client(conf: RabbitMQClientConf) -> pika.channel.Channel:
    while True:
        try:
            credentials = pika.PlainCredentials(
                conf.rabbitmq_username, conf.rabbitmq_password
            )
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    conf.rabbitmq_host, conf.rabbitmq_port, "/", credentials
                )
            )
            channel = connection.channel()
            return RabbitMQClient(connection, channel)
        except pika.exceptions.ConnectionClosed as e:
            print(f"Error connecting to RabbitMQ: {e}")
            print("Config attributes:")
            for attr in dir(conf):
                if "rabbitmq" in attr:
                    print(f"  {attr}: {getattr(conf, attr)}")
            time.sleep(1)
        except Exception as e:
            print(f"Error creating RabbitMQ client: {e}")
            print("Config attributes:")
            for attr in dir(conf):
                if "rabbitmq" in attr:
                    print(f"  {attr}: {getattr(conf, attr)}")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print(f"Exception type: {exc_type.__name__}")
            print(f"Exception message: {exc_value}")
            print("Traceback details:")
            traceback.print_tb(exc_traceback)
            time.sleep(1)
