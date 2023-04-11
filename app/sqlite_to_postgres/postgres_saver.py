from psycopg2.extensions import connection as _connection


class PostgresSaver:
    """Класс для сохранения данных в бд
    Принимает словарь из sqllite_extractor.py со значениями из dataclasses
    проходит циклом, каждые 100 записей добавляет в postgres.
    """

    def __init__(self, pg_conn: _connection):
        self.conn = pg_conn
        self.cursor = self.conn.cursor()
        self.counter = 0

    def mogrify_create(self, data) -> str:
        ss = " ,%s"
        args = ','.join(
            self.cursor.mogrify(
                f"(%s{ss * (len(data[0].__dict__) - 1)})",
                list(value for _, value in item.__dict__.items())
            ).decode() for item in data
        )
        return args

    def save_all_data(self, data: dict) -> bool:
        for table in data:
            batch = 100
            self.cursor.execute(f"""
                                    TRUNCATE content.{table}
                                    CASCADE;
                                     """)
            for i in range(0, len(data[table]) + batch, batch):
                data_save = data[table][i: i + batch]
                if data_save:
                    self.cursor.execute(f"""
                        INSERT INTO content.{table} ({', '.join(i for i in data[table][0].__annotations__)})
                        VALUES {self.mogrify_create(data_save)}
                        ON CONFLICT DO NOTHING
                        """)
                    self.conn.commit()
        return True

# execute_batch в данном случае не особо даст прироста, поскольку и так сохранение батчами прописано.
# но способ запомнил, буду использовать.
