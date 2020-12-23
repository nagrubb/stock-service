import os
from typing import Dict


class Config(object):
    def __init__(self, config: Dict[str, str]) -> None:
        self._config = {}
        self._config['ALPHA_VANTAGE_API_KEY'] = self.__read_file_contents(
            config['ALPHA_VANTAGE_API_KEY_FILE'])
        self._config['REDIS_SERVER'] = config.get('REDIS_SERVER')
        self._config['REDIS_PORT'] = int(config.get('REDIS_PORT'))
        self._config['CACHE_DURATION_MINS'] = int(
            config.get('REDIS_CACHE_DURATION_IN_MINUTES'))

    def __get_property(self, property_name: str) -> object:
        return self._config.get(property_name)

    def __read_file_contents(self, filename: str) -> str:
        return open(filename, 'r').read()

    def print(self) -> None:
        print(self._config)

    @property
    def alpha_vantage_api_key(self) -> str:
        return self.__get_property('ALPHA_VANTAGE_API_KEY')

    @property
    def redis_server(self) -> str:
        return self.__get_property('REDIS_SERVER')

    @property
    def redis_port(self) -> int:
        return self.__get_property('REDIS_PORT')

    @property
    def cache_duration_in_minutes(self) -> int:
        return self.__get_property('CACHE_DURATION_MINS')
