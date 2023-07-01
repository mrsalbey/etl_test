import sqlite3
from contextlib import contextmanager
from dataclasses import astuple
from dataclasses import fields as dataclass_fields
from typing import ContextManager, Generator, Tuple

from models import SQLITE_TABLES_FIELDS, TABLE_CLASS_MAPPING, TABLE_FIELDS_MAPPING
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values
from settings import BATCH_SIZE, SCHEMA_NAME


@contextmanager
def conn_context(db_path: str) -> ContextManager[sqlite3.Connection]:
    """
    Контекстное управление для соединения с базой данных SQLite.

    Args:
        db_path (str): Путь к файлу базы данных SQLite.

    Yields:
        sqlite3.Connection: Соединение с базой данных SQLite.

    Example:
        with conn_context('mydatabase.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM mytable')
            rows = cursor.fetchall()
            for row in rows:
                print(row)
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection) -> None:
        """
            Инициализирует объект SQLiteExtractor.

            Args:
                connection (sqlite3.Connection): Соединение с базой данных SQLite.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    def extract_movies(self) -> Generator[Tuple[list, str], None, None]:
        """
        Извлекает фильмы из базы данных SQLite.

        Yields:
            Tuple[list, str]: Пакет данных (список) и имя таблицы, из которой данные были извлечены.
        """
        for table_name, class_data in TABLE_CLASS_MAPPING.items():
            query = 'SELECT {0} FROM {1};'.format(SQLITE_TABLES_FIELDS[table_name], table_name)
            self.cursor.execute(query)
            fields = [field.name for field in dataclass_fields(class_data)]
            while batch := self.cursor.fetchmany(BATCH_SIZE):
                for index, row in enumerate(batch):
                    batch[index] = class_data(**{key: value for key, value in dict(row).items() if key in fields})
                yield batch, table_name


class PostgresSaver:
    def __init__(self, connection: _connection) -> None:
        """
        Инициализирует объект PostgresSaver.

        Args:
            connection (psycopg2.extensions.connection): Соединение с базой данных PostgreSQL.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.schema_name = SCHEMA_NAME
        self._truncate_tables()

    def _truncate_tables(self) -> None:
        """
        Очищает все таблицы в схеме PostgreSQL.
        """
        for table in TABLE_CLASS_MAPPING.keys():
            query = f'TRUNCATE TABLE {self.schema_name}.{table} CASCADE;'
            self.cursor.execute(query)

    def save_all_data(self, batch, table) -> None:
        """
        Сохраняет все данные пакета в указанную таблицу.

        Args:
            batch (List[Any]): Пакет данных (список) для сохранения.
            table (str): Имя таблицы, в которую будут сохранены данные.
        """
        fields = [field.name for field in dataclass_fields(batch[0])]
        fields = [TABLE_FIELDS_MAPPING.get(field, field) for field in fields]
        fields = ', '.join(fields)
        values = [astuple(row) for row in batch]
        insert_query = f"""
            INSERT INTO {self.schema_name}.{table} ({fields})
            VALUES %s
            ON CONFLICT (id) DO NOTHING;"""
        execute_values(self.cursor, insert_query, values)
        self.connection.commit()
