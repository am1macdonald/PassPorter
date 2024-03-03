import secrets

from pydantic import BaseModel

from controllers.DatabaseController import DatabaseController
from models.BaseDBModel import DBModel
from models.User import User


class TokenRequest(BaseModel):
    authorization: str
    client_secret: str
    client_id: str


class Authorization:
    def __init__(self, client_id: str = None, authorization: str = None):
        self.db = DatabaseController()
        self.client_id = client_id
        self._client = self._fetch() if client_id != '' else None

    def add(self):
        print("adding client")

    def get(self):
        return self._client

    def add_authorization(self, user: User, redirect: str, scope: str):
        auth_user = user.get_user()
        code = secrets.token_urlsafe(64)
        sql = '''
        INSERT INTO public.authorization_codes
            (code, client_id, user_id, redirect, "scope")
        VALUES
            (%s, %s, %s, %s, %s)
        RETURNING code;
        '''
        vals = (code, self.client_id, auth_user.user_id, redirect, scope)
        self.db.connect()
        res = self.db.arbitrary(sql, vals)
        self.db.commit()
        self.db.disconnect()
        return res[0][0] if len(res) > 0 else None

    def _fetch(self):
        self.db.connect()
        sql = f'''
        SELECT 
            *
        FROM 
            public.authorization_codes
        WHERE
            code = %s;
                '''
        vals = (self.client_id,)
        res = self.db.arbitrary(sql, vals)
        client = DBAuth.from_row(res)[0] if len(res) > 0 else None
        self.db.disconnect()
        return client
