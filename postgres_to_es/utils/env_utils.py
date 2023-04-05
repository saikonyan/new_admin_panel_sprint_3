from pydantic import (BaseSettings, Field)
import dotenv

dotenv.load_dotenv()  # для дебага вне докера


class Dsn(BaseSettings):
    dbname: str = Field('movies_database', env='POSTGRES_DB')
    user: str = Field('app', env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field('127.0.0.1', env='DB_HOST')
    port: str = Field(5432, env='DB_PORT')


class EsBaseUrl(BaseSettings):
    """ 
    определяет host и port у ElasticSearch
    """
    es_host: str = Field(..., env='ES_HOST')
    es_port: str = Field(9200, env='ES_PORT')

    def get_url(self):
        '''
        возвращает url ElasticSearch
        '''
        return 'http://{}:{}'.format(self.es_host, self.es_port)


class BaseConfig(BaseSettings):
    chunk_size: int = Field(50, env='CHUNK_SIZE')
    sleep_time: float = Field(60.0, env='ETL_SLEEP')
    es_base_url: str = EsBaseUrl().get_url()
    dsn: dict = Dsn().dict()
