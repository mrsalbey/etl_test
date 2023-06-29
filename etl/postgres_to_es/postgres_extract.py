


class PostgresExtractor:
    """
    Класс для извлечения данных из базы данных PostgreSQL.

    Атрибуты:
        LIMIT (int): Максимальное количество записей, возвращаемых при извлечении данных.
        connection (psycopg2.extensions.connection): Соединение с базой данных PostgreSQL.
        cursor (psycopg2.extensions.cursor): Курсор для выполнения SQL-запросов.
    """

    LIMIT = 100

    def __init__(self, connection) -> None:
        """
        Инициализирует объект PostgresExtractor.

        Args:
            connection (psycopg2.extensions.connection): Соединение с базой данных PostgreSQL.
        """
        self.connection = connection
        self.cursor = self.connection.cursor()

    @staticmethod
    def extract_data(query: str, curs) -> list:
        """
        Извлекает данные из базы данных с помощью SQL-запроса.

        Args:
            query (str): SQL-запрос для извлечения данных.
            cursor (psycopg2.extensions.cursor): Курсор для выполнения SQL-запроса.

        Returns:
            list: Список извлеченных данных.
        """
        curs.execute(query)
        data = curs.fetchall()
        return data
