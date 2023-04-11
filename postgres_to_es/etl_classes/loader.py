import json

import elasticsearch.exceptions
from elasticsearch import helpers,ConnectionError

from utils.connection_util import elastic_search_connection
from utils.backoff_util import backoff

from .indices import settings, mappings

class Loader:
    def __init__(self, dsn, logger) -> None:
        self.dsn = dsn
        self.logger = logger
        # при первичной инициализации класса Loader создадим (если нет) индекс movies в ElasticSearch
        self.create_index('movies')

    @backoff((ConnectionError,))
    def create_index(self, index_name: str) -> None:
        """Создание ES индекса."""

        # подключившись к ES
        with elastic_search_connection(self.dsn) as es:
            if not es.ping():
                raise elasticsearch.exceptions.ConnectionError
            # если нет индекса
            if not es.indices.exists(index='movies'):
                # создаем индекс movies
                es.indices.create(index=index_name, settings=settings, mappings=mappings)
                self.logger.info(f"Create index {index_name}:"
                                 f"{json.dumps(settings, indent=2)} и {json.dumps(mappings, indent=2)} ")

    def load(self, data: list[dict]) -> None:
        """Загружаем данные пачками в ElasticSearch """
        actions = [{'_index': 'movies', '_id': row['id'], '_source': row, } for row in data]
        # подключившись к ElasticSearch
        with elastic_search_connection(self.dsn) as es:
            # используя встроенные методы библиотеки elasticsearch грузим данные в ElasticSearch
            helpers.bulk(es, actions)
            self.logger.info(f'loaded {len(data)} strings')
