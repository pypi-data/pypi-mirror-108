from typing import Union, Optional

from pika import PlainCredentials, ConnectionParameters


class RabbitConfig:

    def __init__(
            self,
            host: Optional[str] = None,
            port: Optional[Union[str, int]] = None,
            exchange: Optional[str] = None,
            virtual_host: Optional[str] = None,
            credentials: Optional[PlainCredentials] = None
    ) -> None:
        self.host = host or '127.0.0.1'
        self.port = port or '5762'
        self.exchange = exchange or 'default'
        self.virtual_host = virtual_host or '/'
        self.credentials = credentials or PlainCredentials('guest', 'guest')
        self.params = ConnectionParameters(
            host=host,
            port=int(port),
            virtual_host=virtual_host,
            credentials=credentials
        )

    @staticmethod
    def from_dict(dictionary: dict[str, any]) -> 'RabbitConfig':
        host = dictionary.get('host')
        port = dictionary.get('port')
        exchange = dictionary.get('exchange')
        virtual_host = dictionary.get('virtual_host')
        credentials = PlainCredentials(
            dictionary.get('username') or dictionary.get('user') or 'guest',
            dictionary.get('password') or dictionary.get('pass') or 'guest'
        )
        return RabbitConfig(host, port, exchange, virtual_host, credentials)
