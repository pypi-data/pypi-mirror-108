# Snacks

Snacks is a wrapper around [pika](https://pypi.org/project/pika/) to
provide a convenient interface to publish/subscribe to queues in
RabbitMQ.

## Example

```python
from snacks.rabbit import RabbitApp

# Setup
rabbit = RabbitApp()
queue = 'snacks'
key = 'snackey'
rabbit.exchange_declare(exchange_type='topic', durable=True)
rabbit.queue_declare(queue=queue, durable=True)
rabbit.queue_bind(queue=queue, routing_key=key)


@rabbit.listener([queue])
def listen(event: str) -> str:
    print(f'Received request: {event}')
    return 'Rabbits and pikas are snacks.'


if __name__ == '__main__':
    r = rabbit.publish_and_receive('To a python.', key, serialize=bytes.decode)
    print(f'Received response: {r}')
```
