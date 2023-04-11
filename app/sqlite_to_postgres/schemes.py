from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass(frozen=True)
class FilmWork:
    title: str
    description: str
    creation_date: datetime
    file_path: str
    type: str
    created: datetime
    modified: datetime
    #certificate: str = field(default='None')
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Genre:
    name: str
    description: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class GenreFilmWork:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class Person:
    full_name: str
    created: datetime
    modified: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class PersonFilmWork:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

def _test():
    assert add('1', '1') == 2

if __name__ == '__main__':
    _test()
