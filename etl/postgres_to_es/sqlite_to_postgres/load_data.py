import os
import sqlite3
from contextlib import closing
from pathlib import Path

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from settings import DSL, SQLITE_DB_NAME
from utils import PostgresSaver, SQLiteExtractor, conn_context


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """
    Загружает данные из SQLite в PostgreSQL.

    Args:
        connection (sqlite3.Connection): Соединение с базой данных SQLite.
        pg_conn (psycopg2.extensions.connection): Соединение с базой данных PostgreSQL.
    """
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    for batch, table_name in sqlite_extractor.extract_movies():
        postgres_saver.save_all_data(batch, table_name)


if __name__ == '__main__':
    sqlite_db = os.path.join(Path(__file__).parent.absolute(), SQLITE_DB_NAME)
    with conn_context(sqlite_db) as sqlite_conn, closing(psycopg2.connect(**DSL, cursor_factory=DictCursor)) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
