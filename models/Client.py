import bcrypt

from controllers.DatabaseController import DatabaseController
from models.BaseDBModel import DBModel


class DBClient(DBModel):
    client_id: str
    client_name: str
    client_secret_hash: str
    hostname: str
    redirect: str


class Client:
    def __init__(self, client_id: str):
        self.db = DatabaseController()
        self._client = self._fetch(client_id) if client_id else None

    def add(self):
        print("adding client")

    def get(self):
        return self._client

    def validate(self, secret: str):
        return bcrypt.checkpw(secret.encode(), self._client.client_secret_hash.encode())

    def _fetch(self, client_id):
        self.db.connect()
        sql = f'''
            select
                client_id,
                client_name,
                client_secret_hash,
                hostname,
                redirect
            from
                clients
            join client_sites
                 using("client_id")
            where
                client_id = %s;'''

        vals = (client_id,)
        res = self.db.arbitrary(sql, vals)
        client = DBClient.from_row(res[0]) if len(res) > 0 else None
        self.db.disconnect()
        return client
