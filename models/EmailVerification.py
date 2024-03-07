import os
from datetime import datetime

from models.BaseDBModel import DBModel


class DBEmailVerification(DBModel):
    id: int
    user_id: int
    confirmation_token: str
    expiration_date: datetime
    verification_status: bool
    confirmation_date: datetime
    attempts: int


class EmailVerification:
    def __init__(self, token=None, conn=None):
        self._token = token
        self._conn = conn
        self._underlying: DBEmailVerification = self._fetch()

    def add(self, user_id: int):
        if self._underlying is not None:
            raise ValueError('Already exists!')
        cur = self._conn.cursor()
        sql = '''
        INSERT INTO public.email_verification
        (user_id)
        VALUES(%s)
        RETURNING *;
        '''
        vals = (user_id,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            self._conn.commit()
            self._underlying = DBEmailVerification.from_row(res)

    def exists(self):
        return self._underlying is not None

    def get_link(self):
        if not self._underlying:
            raise ValueError("Token does not exist")
        return f'{os.environ["BASE_URL"]}/verify-email/{self._underlying.confirmation_token}'

    def _fetch(self):
        cur = self._conn.cursor()
        sql = '''
        SELECT * FROM public.email_verification
        WHERE "confirmation_token" = %s;
        '''
        vals = (self._token,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        return DBEmailVerification.from_row(res) if res else None
