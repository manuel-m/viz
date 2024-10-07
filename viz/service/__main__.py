from viz.conf import Conf
from viz.service.daemon import Daemon


from viz.logger.rabbitLogger import create_rabbitmq_logger, RabbitMQLogsConf
from viz.broker.rabbitClient import create_rabbitmq_client, RabbitMQClientConf

import sys, os


def main() -> None:
    rabbitmq_client_emitter = create_rabbitmq_client(RabbitMQClientConf())

    channel = rabbitmq_client_emitter.channel
    channel.queue_declare(queue="hello")
    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
    print(" [x] Sent 'Hello World!'")

    logger_conf = RabbitMQLogsConf(logger_name="viz-daemon")

    logger = create_rabbitmq_logger(
        logger_conf,
        rabbitmq_client_emitter,
    )

    logger.info("yeah")

    print("logger ok")

    daemon = Daemon(Conf({"debug": False, "timeout": 10}))
    daemon.start()
    daemon.run()
    daemon.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by keyboard")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
