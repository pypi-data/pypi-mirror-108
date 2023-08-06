import ast
import json
import logging
import numbers
import threading
import uuid
from inspect import signature
from typing import Optional, Any, Callable, Mapping, Union

from pika import (BlockingConnection, BasicProperties, ConnectionParameters,
                  PlainCredentials)
from pika.adapters.blocking_connection import BlockingChannel
from pika.exchange_type import ExchangeType
from pika.frame import Method
from pika.spec import Basic, Queue

__all__ = ('RabbitApp',)
log = logging.getLogger('snacks')


# TODO django_rest_framework serializer support?
# TODO default request/response serializers?
class RabbitApp:
    """A class to interface with RabbitMQ."""

    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[Union[str, int]] = None,
            default_exchange: Optional[str] = None,
            virtual_host: Optional[str] = None,
            username: Optional[str] = None,
            password: Optional[str] = None,
    ) -> None:
        self.host = host or '127.0.0.1'
        self.port = port or '5762'
        self.default_exchange = default_exchange or ''
        self.virtual_host = virtual_host or '/'
        log.info('RabbitApp configured.')
        log.debug('host=%s', self.host)
        log.debug('port=%s', self.port)
        log.debug('default_exchange=%s', self.default_exchange)
        log.debug('virtual_host=%s', self.virtual_host)
        if username and password:
            self.credentials = PlainCredentials(username, password)
        else:
            self.credentials = PlainCredentials('guest', 'guest')
        self.params = ConnectionParameters(
            host=host,
            port=int(port),
            virtual_host=virtual_host,
            credentials=self.credentials
        )
        self.connection = BlockingConnection(self.params)
        self.channel: BlockingChannel = self.connection.channel()

    @staticmethod
    def from_dict(dictionary: dict[str, any]) -> 'RabbitApp':
        return RabbitApp(
            dictionary.get('host'),
            dictionary.get('port'),
            dictionary.get('exchange'),
            dictionary.get('virtual_host'),
            dictionary.get('username') or dictionary.get('user') or 'guest',
            dictionary.get('password') or dictionary.get('pass') or 'guest'
        )

    def exchange_declare(
            self,
            exchange: Optional[str] = None,
            exchange_type: str = ExchangeType.direct,
            passive: bool = False,
            durable: bool = False,
            auto_delete: bool = False,
            internal: bool = False,
            arguments: Optional[Mapping[str, Any]] = None
    ) -> Method:
        """Wrapper for pika.BlockingChannel exchange_declare method.

        This method creates an exchange if it does not already exist,
        and if the exchange exists, verifies that it is of the correct
        and expected class.

        If passive set, the server will reply with Declare-Ok if the
        exchange already exists with the same name, and raise an error
        if not and if the exchange does not already exist, the server
        MUST raise a channel exception with reply code 404 (not found).

        :param exchange: The exchange name consists of a non-empty
            sequence of these characters: letters, digits, hyphen,
            underscore, period, or colon.
        :param exchange_type: The exchange type to use.
        :param passive: Perform a declare or just check to see if it
            exists.
        :param durable: Survive a reboot of RabbitMQ.
        :param auto_delete: Remove when no more queues are bound to it.
        :param internal: Can only be published to by other exchanges.
        :param arguments: Custom key/value pair arguments for the
            exchange.
        :return: Method frame from the Exchange.Declare-ok response.
        """
        return self.channel.exchange_declare(
            exchange or self.default_exchange,
            exchange_type,
            passive,
            durable,
            auto_delete,
            internal,
            arguments
        )

    def queue_declare(
            self,
            queue: str,
            passive: bool = False,
            durable: bool = False,
            exclusive: bool = False,
            auto_delete: bool = False,
            arguments: Optional[Queue.DeclareOk] = None,
    ) -> Method:
        """Wrapper for pika.BlockingChannel queue_declare method.

        Declare queue, create if needed. This method creates or
        checks a queue. When creating a new queue the client can specify
        various properties that control the durability of the queue and
        its contents, and the level of sharing for the queue. Use an
        empty string as the queue name for the broker to auto-generate
        one. Retrieve this auto-generated queue name from the returned
        spec.Queue.DeclareOk method frame.

        :param queue: The queue name; if empty string, the broker will
            create a unique queue name.
        :param passive: Only check to see if the queue exists and raise
            `ChannelClosed` if it doesn't.
        :param durable: Survive reboots of the broker.
        :param exclusive: Only allow access by the current connection.
        :param auto_delete: Delete after consumer cancels or
            disconnects.
        :param arguments: Custom key/value arguments for the queue.
        :return: Method frame from the Queue.Declare-ok response
        """
        return self.channel.queue_declare(
            queue,
            passive,
            durable,
            exclusive,
            auto_delete,
            arguments
        )

    def queue_bind(
            self,
            queue: str,
            exchange: Optional[str] = None,
            routing_key: Optional[str] = None,
            arguments: Optional[Mapping[str, Any]] = None
    ) -> Method:
        """ Wrapper for pika.BlockingChannel queue_bind method.

        Bind the queue to the specified exchange.

        :param queue: The queue to bind to the exchange.
        :param exchange: The source exchange to bind to.
        :param routing_key: The routing key to bind on.
        :param arguments: Custom key/value pair arguments for the
            binding.
        :return: Method frame from the Queue.Bind-ok response.
        """
        return self.channel.queue_bind(
            queue,
            exchange or self.default_exchange,
            routing_key,
            arguments
        )

    def publish(
            self,
            body: Any,
            routing_key: str,
            exchange: Optional[str] = None,
            **kwargs
    ) -> None:
        """Publish message to a rabbit queue with the given routing key.

        :param body: The message to publish.
        :param routing_key: The routing key.
        :param exchange: Exchange to publish to.
        :param kwargs: Keyword args to pass to pika publish.
        """
        log.debug('Publishing key=%s msg=%s', routing_key, body)
        self.channel.basic_publish(
            exchange=exchange or self.default_exchange,
            routing_key=routing_key,
            body=_def_serialize(body),
            **kwargs
        )

    def publish_and_receive(
            self,
            body: Any,
            routing_key: str,
            exchange: Optional[str] = None,
            serialize: Optional[Callable] = None,
            time_limit: int = 60,
            headers: Optional[dict[str, Any]] = None
    ) -> Any:
        """Publish message to a rabbit queue with the given routing key.

        :param body: The message to publish.
        :param routing_key: The routing key.
        :param exchange: Exchange to publish to.
        :param serialize: Callable to serialize response bodies.
        :param time_limit: Number of seconds to wait for a response.
        :param headers: Headers to publish with.
        """
        log.debug('Publishing key=%s msg=%s', routing_key, body)
        response: Optional[bytes] = None
        corr_id = str(uuid.uuid4())

        def _on_response(
                _channel: BlockingChannel,
                _method: Basic.Deliver,
                props: BasicProperties,
                resp_body: bytes
        ) -> None:
            nonlocal response
            if props.correlation_id == corr_id:
                log.debug('RPC response from %s is %s', routing_key, resp_body)
                response = resp_body

        result = self.channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=callback_queue,
            on_message_callback=_on_response,
            auto_ack=True
        )
        self.channel.basic_publish(
            exchange=exchange or self.default_exchange,
            routing_key=routing_key,
            properties=BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
                headers=headers
            ),
            body=_def_serialize(body)
        )
        self.connection.process_data_events(time_limit=time_limit)
        return serialize(response) if serialize else response

    def listener(
            self,
            queues: list[str],
            serialize=None
    ) -> Callable:
        """Decorate a function to make it a rabbit consumer.

        The decorated function can have as parameters, the message body,
        the method, the properties, or no parameters.

        A new channel and thread is created for each consumer.

        :param queues: The queues to consume from.
        :param serialize: Callable to serialize message bodies.
        :return: Function decorated to be a rabbit consumer.
        """
        # Threads cannot share a connection or channel.
        channel = BlockingConnection(self.params).channel()

        def wrapper(fun: Callable) -> None:
            original_name = fun.__name__
            for queue in queues:
                fun.__name__ = f'listener_{queue}'
                _listen(channel, queue, fun, serialize)
                log.info(
                    'Function %s subscribed to queue %s.',
                    original_name,
                    queue
                )
            thread = threading.Thread(target=_consume, args=(channel,))
            thread.daemon = True
            thread.start()

        return wrapper


def _listen(
        channel: BlockingChannel,
        queue: str,
        fun: Callable,
        serialize: Optional[Callable] = None
) -> None:
    sig = signature(fun)

    def callback(
            ch: BlockingChannel,
            method: Basic.Deliver,
            properties: BasicProperties,
            body: bytes
    ) -> None:
        log.debug('Queue %s received %s.', queue, body)
        kwargs: dict[str, Any] = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                kwargs[name] = None
            elif param.annotation == BlockingChannel:
                kwargs[name] = ch
            elif param.annotation == method:
                kwargs[name] = method
            elif param.annotation == BasicProperties:
                kwargs[name] = properties
            elif param.annotation == str:
                kwargs[name] = body.decode('utf-8')
            elif param.annotation in {list, tuple, set, dict}:
                kwargs[name] = ast.literal_eval(body.decode('UTF-8'))
            elif param.annotation == bytes:
                kwargs[name] = body
            elif param.annotation in {int, float}:
                kwargs[name] = param.annotation(body)
            elif 'from_json' in dir(param.annotation):
                kwargs[name] = param.annotation.from_json(body)
            else:
                try:
                    kwargs[name] = json.loads(body)
                except json.decoder.JSONDecodeError:
                    kwargs[name] = body
        # noinspection PyBroadException
        try:
            resp = fun(**kwargs)
            if properties.reply_to:
                ch.basic_publish(
                    exchange='',
                    routing_key=properties.reply_to,
                    properties=BasicProperties(
                        correlation_id=properties.correlation_id
                    ),
                    body=serialize(resp) if serialize else _def_serialize(resp)
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            log.exception(msg=f'{type(e).__name__}: {e}', exc_info=e)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue,
        auto_ack=not sig.return_annotation,
        on_message_callback=callback
    )


def _consume(channel: BlockingChannel) -> None:
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        channel.close()


def _def_serialize(body: Any) -> bytes:
    if 'to_json' in dir(body):
        return body.to_json().encode()
    elif isinstance(body, numbers.Number):
        return str(body).encode()
    else:
        return body
