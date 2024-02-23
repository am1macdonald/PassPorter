import os

import psycopg2


class DatabaseController:
    def __init__(self):
        print("new DB Controller")
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = psycopg2.connect(dbname=os.environ["PGDATABASE"],
                                user=os.environ["PGUSER"],
                                password=os.environ["PG_PASSWORD"],
                                host=os.environ["PGHOST"],
                                port=os.environ["PGPORT"])

        # Open a cursor to perform database operations
        self.cursor = self.connection.cursor()
