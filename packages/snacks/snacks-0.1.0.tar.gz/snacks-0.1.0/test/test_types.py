import os
from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json
from pika import BlockingConnection, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel

from snacks.rabbit import RabbitApp
from snacks.rabbit_config import RabbitConfig

# Initial setup of configuration and Rabbit class.
config = RabbitConfig(
    host='localhost',
    port=5672,
    exchange='snacks',
    virtual_host='/',
    credentials=PlainCredentials(
        os.environ.get('AMQP_USERNAME') or 'guest',
        os.environ.get('AMQP_PASSWORD') or 'guest'
    )
)
rabbit = RabbitApp(config)
# Setup queues to use.
str_queue = 'snack_str'
bytes_queue = 'snack_bytes'
event_queue = 'snack_event'
str_key = 'str_key'
bytes_key = 'bytes_key'
event_key = 'event_key'
mq_conn = BlockingConnection(rabbit.config.params)
channel: BlockingChannel = mq_conn.channel()
channel.exchange_declare(
    exchange=rabbit.config.exchange,
    exchange_type='topic',
    durable=True
)
for key, queue in {
    str_key: str_queue,
    bytes_key: bytes_queue,
    event_key: event_queue
}.items():
    channel.queue_declare(queue=queue, durable=True)
    channel.queue_bind(
        exchange=rabbit.config.exchange,
        queue=queue,
        routing_key=key
    )


@dataclass_json
@dataclass
class User:
    id: int
    first: str
    last: str


@dataclass_json
@dataclass
class Event:
    type: str
    body: Any


@rabbit.listener([str_queue, bytes_queue])
def str_listen(string: str) -> None:
    print(f'Received message: {string}')


@rabbit.listener([event_queue])
def event_listen(event: Event) -> None:
    print(f'Received message: {event}')


if __name__ == '__main__':
    rabbit.publish(Event('parse', User(1, 'Snacky', 'McSnackface')), event_key)
    rabbit.publish('Eat this string.', str_key)
    rabbit.publish(b'Nom these bytes.', bytes_key)
    rabbit.publish(19, str_key)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Exiting...')
