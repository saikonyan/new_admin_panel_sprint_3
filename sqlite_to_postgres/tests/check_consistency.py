import psycopg2
import sqlite3
from psycopg2.extensions import connection as _connection
from sqlite_to_postgres.sqlite_extractor import SQLiteExtractor


db_path = 'db.sqlite'
dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}


def chech_etl(connection: sqlite3.Connection, pgconn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    check_list = ['genre', 'film_work', 'person', 'genre_film_work', 'person_film_work']
    cursor_pg = pgconn.cursor()
    sqlite_extractor = SQLiteExtractor(connection)
    data = sqlite_extractor.load_all()
    for table in check_list:
        cursor_pg.execute(f"""SELECT * FROM content.{table}""")
        result_pg = sum(list(map(list, cursor_pg.fetchall())), [])
        result_sqlite = data[table]
        for row in result_sqlite:
            n = 0
            for item in list(row.__dict__.items()):
                if item[1] not in result_pg:
                    n += 1
            assert n != len(list(row.__dict__.items())),\
                f'Строка {list(row.__dict__.items())} не была перенесена в таблицу {table}'
        print(f'В таблице {table} все строки перенесены корректно')


if __name__ == '__main__':

    with sqlite3.connect(db_path) as sqlite_conn, psycopg2.connect(**dsl) as pg_conn:
        chech_etl(sqlite_conn, pg_conn)
