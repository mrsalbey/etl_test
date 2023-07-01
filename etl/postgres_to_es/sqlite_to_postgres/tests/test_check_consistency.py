import sqlite3
from sqlite3 import Connection as SQLiteConnection
from typing import Generator

import psycopg2
import pytest
from psycopg2.extensions import connection as PostgresConnection


class TestDatabase:
    """
    Словарь содержит перечень таблиц приложения.
    Ключ - наименование таблицы.
    Значения - словарь полей таблицы.
    Например, {'field_name_sqlite': 'field_name_postgres',}
    """

    column_mapping = {
        'genre': {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'created_at': 'created',
            'updated_at': 'modified',
        },
        'film_work': {
            'id': 'id',
            'title': 'title',
            'description': 'description',
            'creation_date': 'creation_date',
            'file_path': 'file_path',
            'rating': 'rating',
            'type': 'type',
            'created_at': 'created',
            'updated_at': 'modified',
        },
        'person': {'id': 'id', 'full_name': 'full_name', 'created_at': 'created', 'updated_at': 'modified'},
        'genre_film_work': {
            'id': 'id',
            'film_work_id': 'film_work_id',
            'genre_id': 'genre_id',
            'created_at': 'created',
        },
        'person_film_work': {
            'id': 'id',
            'film_work_id': 'film_work_id',
            'person_id': 'person_id',
            'role': 'role',
            'created_at': 'created',
        },
    }

    @pytest.fixture(scope='module')
    def sqlite_connection(self) -> Generator[SQLiteConnection, None, None]:
        """Фикстура, предоставляющая подключение к SQLite базе данных."""
        conn = sqlite3.connect('./db.sqlite')
        yield conn
        conn.close()

    @pytest.fixture(scope='module')
    def postgres_connection(self) -> Generator[PostgresConnection, None, None]:
        """Фикстура, предоставляющая подключение к PostgreSQL базе данных."""
        conn = psycopg2.connect(host='127.0.0.1', port='5432', dbname='movies_database', user='app', password='123qwe')
        yield conn
        conn.close()

    @pytest.fixture(scope='class')
    def schema_name(self) -> str:
        """Фикстура, возвращающая имя схемы в PostgreSQL базе данных."""
        return 'content'

    @pytest.mark.parametrize('table_name', column_mapping.keys())
    def test_table_integrity(
        self,
        sqlite_connection: SQLiteConnection,
        postgres_connection: PostgresConnection,
        schema_name: str,
        table_name: str,
    ) -> None:
        """Тест проверки целостности данных в таблице между SQLite и PostgreSQL базами данных.

        Args:
            sqlite_connection (sqlite3.Connection): Подключение к SQLite базе данных.
            postgres_connection (psycopg2.extensions.connection): Подключение к PostgreSQL базе данных.
            schema_name (str): Имя схемы в PostgreSQL базе данных.
            table_name (str): Имя таблицы для проверки целостности.

        Raises:
            AssertionError: Если количество записей или значения колонок не совпадают между SQLite и PostgreSQL.
        """
        sqlite_cursor = sqlite_connection.cursor()
        postgres_cursor = postgres_connection.cursor()

        # Проверка количества записей в таблице
        sqlite_cursor.execute(f'SELECT COUNT(*) FROM {table_name};')
        postgres_cursor.execute(f'SELECT COUNT(*) FROM {schema_name}.{table_name};')
        sqlite_count = sqlite_cursor.fetchone()[0]
        postgres_count = postgres_cursor.fetchone()[0]
        assert sqlite_count == postgres_count, f'Количество записей в таблице {table_name} не совпадает'

        # Проверка содержимого записей в таблице
        sqlite_cursor.execute(f'SELECT * FROM {table_name};')
        sqlite_rows = sqlite_cursor.fetchall()
        sqlite_column_names = [description[0] for description in sqlite_cursor.description]
        postgres_cursor.execute(f'SELECT * FROM {schema_name}.{table_name};')
        postgres_rows = postgres_cursor.fetchall()
        postgres_column_names = [description[0] for description in postgres_cursor.description]

        # Проверка значений в колонках
        table_mapping = self.column_mapping[table_name]
        for i in range(len(sqlite_rows)):
            for sqlite_column, postgres_column in table_mapping.items():
                sqlite_column_index = sqlite_column_names.index(sqlite_column)
                postgres_column_index = postgres_column_names.index(postgres_column)
                sqlite_value = sqlite_rows[i][sqlite_column_index]
                postgres_value = postgres_rows[i][postgres_column_index]
                if postgres_column in ['created', 'modified']:
                    sqlite_value = sqlite_value.split('.')[0]
                    try:
                        postgres_value = postgres_value.strftime('%Y-%m-%d %H:%M:%S.%f%z')
                        postgres_value = postgres_value.split('.')[0]
                    except ValueError:
                        # Обработка исключения, если строка не соответствует ожидаемому формату
                        pass
                assert (
                    sqlite_value == postgres_value
                ), f'Значение в колонке {sqlite_column} в таблице {table_name} не совпадает'
