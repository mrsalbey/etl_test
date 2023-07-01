import os

from dotenv import load_dotenv

load_dotenv()

DSL = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('SQL_HOST'),
    'port': os.getenv('SQL_PORT'),
}

SQLITE_DB_NAME = os.getenv('SQLITE_DB_NAME')

BATCH_SIZE = int(os.getenv('BATCH_SIZE'))

SCHEMA_NAME = os.getenv('SCHEMA_NAME')
