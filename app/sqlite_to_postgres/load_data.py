import sqlite3
import psycopg2
import os
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_extractor import SQLiteExtractor
from postgres_saver import PostgresSaver
from dotenv import load_dotenv
load_dotenv()


# Задаём путь к файлу с базой  данных
db_path = 'db.sqlite'


def load_from_sqlite(connection: sqlite3.Connection, p_conn: _connection):

    postgres_saver = PostgresSaver(p_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.load_all()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    db_path = os.environ.get('PATH_SQLITE')
    print(db_path)
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
    sqlite_conn.close()
    pg_conn.close()
