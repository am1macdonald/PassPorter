import psycopg2
import os

class DatabaseController:
    def __init__(self):
        self.connection_string = os.environ["TEST"]
        print(self.connection_string)

