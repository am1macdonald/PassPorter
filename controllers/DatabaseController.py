import os

import psycopg2


class DatabaseController:
    def __init__(self):
        print("new DB Controller")
        self.connection = None
        self.cursor = None

        # Get all table names
        self.connect()

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

    def select(self, columns, table):
        self.cursor.execute(f"SELECT {', '.join(columns)} from {table}")

    def disconnect(self):
        self.cursor.close()
        self.connection.close()
