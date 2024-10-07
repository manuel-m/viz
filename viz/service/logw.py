from viz.conf import Conf

from viz.broker.rabbitClient import create_rabbitmq_client, RabbitMQClientConf
from viz.logger.rabbitLogsConsumer import create_rabbitmq_logs_consumer

import sys, os


def main() -> None:

    rabbitmq_client_consumer = create_rabbitmq_client(RabbitMQClientConf())

    create_rabbitmq_logs_consumer(
        Conf(
            {
                "queue_name": "logs_queue",
            }
        ),
        rabbitmq_client_consumer,
    )

    print("logw started")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
