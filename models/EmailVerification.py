import os
from datetime import datetime

from models.BaseDBModel import DBModel


class DBEmailVerification(DBModel):
    id: int
    user_id: int
    confirmation_token: str
    expiration_date: datetime
    verification_status: bool
    confirmation_date: datetime | None = None
    attempts: int
    isValid: bool


class EmailVerification:
    def __init__(self, user_id=None, token=None, conn=None):
        self._token = token
        self._user_id = user_id
        self._conn = conn
        self._underlying: DBEmailVerification = self._fetch() if token or user_id else None

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

    def is_valid(self):
        return self._underlying.isValid

    def is_expired(self):
        return self._underlying.expiration_date < datetime.now()

    def get_link(self):
        if not self._underlying:
            raise ValueError("Token does not exist")
        return f'{os.environ["BASE_URL"]}/verify-email/{self._underlying.confirmation_token}'

    def consume(self):
        cur = self._conn.cursor()
        sql = '''
        UPDATE public.email_verification
        SET verification_status = true,
        confirmation_date = Now(),
        attempts = attempts + 1
        WHERE "confirmation_token" = %s
        RETURNING *;
        '''
        vals = (self._underlying.confirmation_token,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            self._conn.commit()
        else:
            self._conn.rollback()
        return res is not None

    def _fetch(self):
        cur = self._conn.cursor()
        sql = ''
        vals = ()
        if self._token:
            sql = '''
            SELECT * FROM public.email_verification
            WHERE "confirmation_token" = %s;
            '''
            vals = (self._token,)
        elif self._user_id:
            sql = '''
            SELECT * FROM public.email_verification
            WHERE "user_id" = %s;
            '''
            vals = (self._user_id,)
        if sql != '' and len(vals) == 1:
            cur.execute(sql, vals)
            res = cur.fetchone()
            return DBEmailVerification.from_row(res) if res else None
