import bcrypt

from models.BaseDBModel import DBModel


class DBClient(DBModel):
    client_id: str
    client_name: str
    client_secret_hash: str
    hostname: str
    redirect: str


class Client:
    def __init__(self, client_id: str, conn=None):
        self._conn = conn
        self._client = self._fetch(client_id) if client_id else None

    def add(self):
        print("adding client")

    def get(self):
        return self._client

    def validate(self, secret: str):
        return bcrypt.checkpw(secret.encode(), self._client.client_secret_hash.encode())

    def _fetch(self, client_id):
        cur = self._conn.cursor()
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
        cur.execute(sql, vals)
        res = cur.fetchone()
        return DBClient.from_row(res) if res else None
