from viz.broker.rabbitClient import RabbitMQClient
from viz.conf import Conf


class RabbitMQLogsConsumer:
    def __init__(self, rabbitmq_client: RabbitMQClient):
        self.rabbitmq_client = rabbitmq_client


def callback(ch, method, properties, body):
    print(f"Received log: {body}")


def create_rabbitmq_logs_consumer(conf: Conf, rabbitmq_client: RabbitMQClient):

    consumer = RabbitMQLogsConsumer(rabbitmq_client)
    rabbitmq_client.channel.queue_declare(queue=conf.queue_name, durable=True)
    rabbitmq_client.channel.basic_consume(
        queue="logs_queue", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for logs...")
    rabbitmq_client.channel.start_consuming()

    return consumer
