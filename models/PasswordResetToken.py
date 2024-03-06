from datetime import datetime

from pydantic import SecretStr

from models.BaseDBModel import DBModel
from models.User import DBUser


class DBToken(DBModel):
    id: int
    user_id: int
    reset_token: SecretStr
    expiration_date: datetime
    is_valid: bool


class PasswordResetToken:
    def __init__(self, user: DBUser | None = None, token_str: SecretStr | None = None, conn=None):
        self._conn = conn
        self.user = user
        self.token_str = token_str
        self.token = self._fetch_token()

    def _fetch_token(self) -> DBToken:
        cur = self._conn.cursor()
        sql = ''
        vals = ()
        if self.user:
            sql = 'select * from "password_reset" where "user_id"=%s and "is_valid"=true order by id desc limit 1;'
            vals = (self.user.user_id,)
        elif self.token_str:
            sql = 'select * from "password_reset" where "reset_token"=%s and "is_valid"=true order by id desc limit 1;'
            vals = (self.token_str.get_secret_value(),)
        cur.execute(sql, vals)
        return cur.fetchone()

    def exists(self) -> bool:
        return self.token is not None and self.token.is_valid

    def invalidate(self):
        cur = self._conn.cursor()
        sql = "UPDATE public.password_reset SET is_valid=false WHERE id = %s RETURNING *;"
        vals = (self.token.id,)
        cur.execute(sql, vals)
        if cur.fetchone():
            self._conn.commit()
        else:
            self._conn.rollback()

    def add(self) -> bool:
        cur = self._conn.cursor()
        sql = '''
        INSERT INTO public.password_reset (user_id) SELECT users.user_id FROM users WHERE users.email = %s RETURNING *;
        '''
        vals = (self.user.email,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            self._conn.commit()
            self.token = DBToken.from_row(res)
        else:
            self._conn.rollback()
        return res
