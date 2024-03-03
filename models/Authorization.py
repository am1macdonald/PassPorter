import secrets
from datetime import datetime

from controllers.DatabaseController import DatabaseController
from models.BaseDBModel import DBModel
from models.Client import Client
from models.User import User


class DBAuth(DBModel):
    code: str
    client_id: str
    user_id: int
    redirect: str
    scope: str
    used: bool
    expiration: datetime


class Authorization:
    def __init__(self, authorization: str = None):
        self.db = DatabaseController()
        self._auth: DBAuth = self._fetch(authorization) if authorization else None

    def get(self):
        return self._auth

    def add_authorization(self, user: User, client: Client, redirect: str, scope: str):
        auth_user = user.get_user()
        code = secrets.token_urlsafe(64)
        sql = '''
        INSERT INTO public.authorization_codes
            (code, client_id, user_id, redirect, "scope")
        VALUES
            (%s, %s, %s, %s, %s)
        RETURNING code;
        '''
        vals = (code, client.get().client_id, auth_user.user_id, redirect, scope)
        self.db.connect()
        res = self.db.arbitrary(sql, vals)
        self.db.commit()
        self.db.disconnect()
        return res[0][0] if len(res) > 0 else None

    def mark_used(self):
        sql = '''
        UPDATE public.authorization_codes
            set "used" = true
        WHERE "code" = %s
        RETURNING code;
        '''
        vals = (self._auth.code,)
        self.db.connect()
        res = self.db.arbitrary(sql, vals)
        self.db.commit()
        self.db.disconnect()
        return res[0][0] if len(res) > 0 else None

    def _fetch(self, code):
        self.db.connect()
        sql = f'''
        SELECT 
            *
        FROM 
            public.authorization_codes
        WHERE
            code = %s;
                '''
        vals = (code,)
        res = self.db.arbitrary(sql, vals)
        client = DBAuth.from_row(res[0]) if len(res) > 0 else None
        self.db.disconnect()
        return client
