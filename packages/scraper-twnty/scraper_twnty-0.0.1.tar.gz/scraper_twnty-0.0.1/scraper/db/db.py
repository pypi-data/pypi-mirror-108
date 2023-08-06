from scraper.db.pool import ConnectionPool


class DataBase(ConnectionPool):
    def __init__(self, database, host, username, password):
        super().__init__(database, host, username, password)

    def execute(self, sql, val):
        with self.get_connection() as con:
            cur = con.cursor()
            cur.execute(sql, val)
            con.commit()
