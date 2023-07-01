from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class Table(ABC):
    """
    Абстрактный базовый класс для таблиц.

    Этот класс представляет абстрактную таблицу базы данных.

    Attributes:
        Нет атрибутов.
    """

    pass


@dataclass
class Genre(Table):
    """
    Класс Genre представляет сущность жанра.

    Attributes:
        id (UUID): Идентификатор жанра.
        name (str): Название жанра.
        description (str): Описание жанра.
        created_at (datetime): Дата и время создания записи о жанре.
        updated_at (datetime): Дата и время последнего обновления записи о жанре.

    Inherits:
        Table: Абстрактный базовый класс для таблиц.
    """

    __slots__ = ('id' 'name', 'description', 'created_at', 'updated_at')
    id: UUID
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Person(Table):
    """
    Класс Person представляет сущность человека.

    Attributes:
        id (UUID): Идентификатор человека.
        full_name (str): Полное имя человека.
        created_at (datetime): Дата и время создания записи о человеке.
        updated_at (datetime): Дата и время последнего обновления записи о человеке.

    Inherits:
        Table: Абстрактный базовый класс для таблиц.
    """

    __slots__ = ('id', 'full_name', 'created_at', 'updated_at')
    id: UUID
    full_name: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Filmwork(Table):
    """
    Класс Filmwork представляет сущность фильма.

    Attributes:
        id (UUID): Идентификатор фильма.
        title (str): Название фильма.
        description (str): Описание фильма.
        creation_date (datetime): Дата создания фильма.
        file_path (Optional[str]): Путь к файлу фильма (необязательный).
        rating (float): Рейтинг фильма.
        type (str): Тип фильма.
        created_at (datetime): Дата и время создания записи о фильме.
        updated_at (datetime): Дата и время последнего обновления записи о фильме.

    Inherits:
        Table: Абстрактный базовый класс для таблиц.
    """

    __slots__ = (
        'id',
        'title',
        'description',
        'creation_date',
        'file_path',
        'rating',
        'type',
        'created_at',
        'updated_at',
    )
    id: UUID
    title: str
    description: str
    creation_date: datetime
    file_path: Optional[str]
    rating: float
    type: str
    created_at: datetime
    updated_at: datetime


@dataclass
class GenreFilmwork(Table):
    """
    Класс GenreFilmwork представляет связь между таблицами FilmWork и Genre.

    Attributes:
        id (UUID): Идентификатор жанра фильма.
        film_work_id (UUID): Идентификатор фильма.
        genre_id (UUID): Идентификатор жанра.
        created_at (datetime): Дата и время создания связи.

    Inherits:
        Table: Абстрактный базовый класс для таблиц.
    """

    __slots__ = ('id', 'film_work_id', 'genre_id', 'created_at')
    id: UUID
    film_work_id: UUID
    genre_id: UUID
    created_at: datetime


@dataclass
class PersonFilmwork(Table):
    __slots__ = ('id', 'film_work_id', 'person_id', 'role', 'created_at')
    id: UUID
    film_work_id: UUID
    person_id: UUID
    role: str
    created_at: datetime


TABLE_CLASS_MAPPING = {
    'genre': Genre,
    'person': Person,
    'film_work': Filmwork,
    'genre_film_work': GenreFilmwork,
    'person_film_work': PersonFilmwork,
}

TABLE_FIELDS_MAPPING = {
    'created_at': 'created',
    'updated_at': 'modified',
}

SQLITE_TABLES_FIELDS = {
    'film_work': 'id,title,description,creation_date,file_path,rating,type,created_at,updated_at',
    'genre': 'id,name,description,created_at,updated_at',
    'person': 'id,full_name,created_at,updated_at',
    'genre_film_work': 'id,genre_id,film_work_id,created_at',
    'person_film_work': 'id,film_work_id,person_id,role,created_at',
}
