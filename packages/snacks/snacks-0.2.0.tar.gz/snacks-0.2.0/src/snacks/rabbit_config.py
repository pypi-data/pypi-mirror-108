from typing import Union, Optional

from pika import PlainCredentials, ConnectionParameters


class RabbitConfig:

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

    @staticmethod
    def from_dict(dictionary: dict[str, any]) -> 'RabbitConfig':
        return RabbitConfig(
            dictionary.get('host'),
            dictionary.get('port'),
            dictionary.get('exchange'),
            dictionary.get('virtual_host'),
            dictionary.get('username') or dictionary.get('user') or 'guest',
            dictionary.get('password') or dictionary.get('pass') or 'guest'
        )
