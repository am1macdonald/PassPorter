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
    def __init__(self, user_id: int = None, conn=None):
        self.user_id = user_id
        self._conn = conn
        self._underlying: DBEmailVerification = self._fetch()

    def add(self):
        cur = self._conn.cursor()
        sql = '''

        '''
        vals = ()
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            self._conn.commit()
            self._underlying = DBEmailVerification.from_row(res)

    def _fetch(self):
        cur = self._conn.cursor()
        sql = '''
        
        '''
        vals = None

        cur.execute(sql, vals)
        res = cur.fetchone()
        return DBEmailVerification.from_row(res) if res else None
