import secrets
from datetime import datetime

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
    def __init__(self, authorization: str = None, conn=None):
        self._conn = conn
        self._auth: DBAuth = self._fetch(authorization) if authorization else None

    def get(self):
        return self._auth

    def add_authorization(self, user: User, client: Client, redirect: str, scope: str):
        cur = self._conn.cursor()
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
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            cur.commit()
            return res[0] if res else None

    def mark_used(self):
        cur = self._conn.cursor()
        sql = '''
        UPDATE public.authorization_codes
            set "used" = true
        WHERE "code" = %s
        RETURNING code;
        '''
        vals = (self._auth.code,)
        cur.execute(sql,vals)
        res = cur.fetchone()
        if res:
            cur.commit()
            return res[0] if res else None

    def _fetch(self, code):
        cur = self._conn.cursor
        sql = f'''
        SELECT 
            *
        FROM 
            public.authorization_codes
        WHERE
            code = %s;
                '''
        vals = (code,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        return DBAuth.from_row(res) if res else None
