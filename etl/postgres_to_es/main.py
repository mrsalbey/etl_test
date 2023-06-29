from time import sleep

import psycopg
from postgres_extract import PostgresExtractor
from settings import database_settings
from psycopg.conninfo import make_conninfo
from psycopg.rows import dict_row


def main():
    dsn = make_conninfo(**database_settings.dict())
    print(dsn)
    #with psycopg.connect(dsn, row_factory=dict_row) as conn, conn.cursor() as cur:
    while True:
        sleep(15)


if __name__ == '__main__':
    main()