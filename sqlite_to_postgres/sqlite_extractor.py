import sqlite3

from sqlite_to_postgres.schemes import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork
)


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.conn = connection
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def load_film_work(self) -> list:
        film_work = []
        for row in self.cur.execute('SELECT * FROM film_work'):
            film_work.append(FilmWork(
                title=row['title'],
                description=row['description'],
                creation_date=row['creation_date'],
                file_path=row['file_path'],
                type=row['type'],
                created=row['created_at'],
                modified=row['updated_at'],
                rating=row['rating'],
                id=row['id']
            ))
        return film_work

    def load_genre(self) -> list:
        genre = []
        for row in self.cur.execute('SELECT * FROM genre'):
            genre.append(Genre(
                name=row['name'],
                description=row['description'],
                created=row['created_at'],
                modified=row['updated_at'],
                id=row['id']
            ))
        return genre

    def load_genre_film_fork(self) -> list:
        genre_film_fork = []
        for row in self.cur.execute('SELECT * FROM genre_film_work'):
            genre_film_fork.append(GenreFilmWork(
                film_work_id=row['film_work_id'],
                genre_id=row['genre_id'],
                created_at=row['created_at'],
                id=row['id'],
            ))
        return genre_film_fork

    def load_person(self) -> list:
        person = []
        for row in self.cur.execute('SELECT * FROM person'):
            person.append(Person(
                full_name=row['full_name'],
                created=row['created_at'],
                modified=row['updated_at'],
                id=row['id'],
            ))
        return person

    def load_person_film_work(self) -> list:
        person_film_work = []
        for row in self.cur.execute('SELECT * FROM person_film_work'):
            person_film_work.append(PersonFilmWork(
                film_work_id=row['film_work_id'],
                person_id=row['person_id'],
                role=row['role'],
                created_at=row['created_at'],
                id=row['id'],
            ))
        return person_film_work

    def load_all(self) -> dict:
        return {
            'film_work': self.load_film_work(),
            'genre': self.load_genre(),
            'genre_film_work': self.load_genre_film_fork(),
            'person': self.load_person(),
            'person_film_work': self.load_person_film_work()
        }

# sqlite на миллионы строк вряд ли найдется. И на самом деле я поленился переписовать все методы
# чтобы одновременно грузить и сохранять данные
