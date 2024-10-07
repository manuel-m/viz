import pika
import logging
import json

import logging

from viz.broker.rabbitClient import RabbitMQClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQLogsConf(BaseSettings):
    logger_name: str
    log_level: int = logging.DEBUG
    queue_name: str = "logs_queue"

    model_config = SettingsConfigDict(env_prefix="CONF_")


def create_rabbitmq_logger(conf: RabbitMQLogsConf, rabbitmq_client: RabbitMQClient):
    logger = logging.getLogger(conf.logger_name)
    logger.setLevel(conf.log_level)

    rabbitmq_handler = RabbitMQHandler(
        rabbitmq_client=rabbitmq_client,
        queue_name=conf.queue_name,
        exchange="",  # Directly send to the queue without an exchange
        routing_key=conf.queue_name,
    )

    rabbitmq_handler.setFormatter(JSONFormatter())
    logger.addHandler(rabbitmq_handler)

    return logger


class RabbitMQHandler(logging.Handler):
    def __init__(
        self,
        rabbitmq_client: RabbitMQClient,
        queue_name: str,
        exchange: str = "",
        routing_key: str = "",
    ):
        logging.Handler.__init__(self)
        self.queue_name = queue_name
        self.exchange = exchange
        self.routing_key = routing_key if routing_key else queue_name

        # Set up the RabbitMQ connection
        self.channel = rabbitmq_client.channel

        # Declare the queue (idempotent)
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def emit(self, record):
        try:
            # Format the log record
            log_entry = self.format(record)

            # Send the log entry to RabbitMQ
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=log_entry,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
        except Exception as e:
            print(f"Error sending log to RabbitMQ: {e}")

    def close(self):
        self.channel.close()
        # self.connection.close()
        super().close()


# Custom formatter to send log messages in JSON format
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "level": record.levelname,
            "message": record.msg,
            "timestamp": self.formatTime(record, self.datefmt),
            "module": record.module,
            "funcName": record.funcName,
            "lineNumber": record.lineno,
        }
        return json.dumps(log_entry)
