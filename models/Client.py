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
        self.client_id = client_id
        self._client = self._fetch()

    def add(self):
        print("adding client")

    def get(self):
        return self._client

    def _fetch(self):
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

        vals = (self.client_id,)
        res = self.db.arbitrary(sql, vals)
        client = DBClient.from_row(res[0]) if len(res) > 0 else None
        self.db.disconnect()
        return client
