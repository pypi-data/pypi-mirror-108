from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


class ConnectionPool:
    def __init__(self, database, host, username, password):
        self.db_connection = "dbname='{}' user='{}' host='{}' password='{}'".format(
            database,
            username,
            host,
            password,
            )

        self.connectionpool = self.__get_connection_pool()

    def __get_connection_pool(self):
        connectionpool = SimpleConnectionPool(1,10,dsn=self.db_connection)

        return connectionpool

    @contextmanager
    def get_connection(self):
        con = self.connectionpool.getconn()
        try:
            yield con
        finally:
            self.connectionpool.putconn(con)
