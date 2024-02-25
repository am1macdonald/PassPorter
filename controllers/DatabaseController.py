import os

import psycopg2


class DatabaseController:
    def __init__(self):
        print("new DB Controller")
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(dbname=os.environ["PG_DATABASE"],
                                           user=os.environ["PG_USER"],
                                           password=os.environ["PG_PASSWORD"],
                                           host=os.environ["PG_HOST"],
                                           port=os.environ["PG_PORT"])

        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()

    def insert(self, table: str, columns: [str], vals: tuple):
        s = []
        for n in columns:
            s.append('%s')
        sql = f'INSERT INTO "public".{table} ({", ".join(columns)}) VALUES ({", ".join(s)}) RETURNING *;'
        self.cursor.execute(sql, vals)
        one = self.cursor.fetchone()
        if one:
            self.connection.commit()
        else:
            self.connection.rollback()
        return one

    def select(self, table, columns: [str], vals: tuple, joins: [str] = None, wheres: [str] = None):
        sql = f'SELECT {", ".join(columns)} from "{table}" '
        if joins:
            sql += " join " + ' '.join(joins)
        if wheres:
            sql += " where " + ' '.join(wheres)
        self.cursor.execute(sql.strip() + ';', vals)
        return self.cursor.fetchall()

    def arbitrary(self, sql: str, vals: tuple):
        self.cursor.execute(sql, vals)
        return self.cursor.fetchall()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
