from datetime import datetime

from pydantic import SecretStr

from controllers.DatabaseController import DatabaseController
from models.BaseDBModel import DBModel
from models.User import DBUser


class DBToken(DBModel):
    id: int
    user_id: int
    reset_token: SecretStr
    expiration_date: datetime
    is_valid: bool


class PasswordResetToken:
    def __init__(self, user: DBUser | None = None, token_str: SecretStr | None = None):
        self.db = DatabaseController()
        self.user = user
        self.token_str = token_str
        self.token = self._fetch_token()

    def _fetch_token(self) -> DBToken:
        self.db.connect()
        query = ''
        params = ()
        if self.user:
            query = 'select * from "password_reset" where "user_id"=%s and "is_valid"=true order by id desc limit 1;'
            params = (self.user.user_id,)
        elif self.token_str:
            query = 'select * from "password_reset" where "reset_token"=%s and "is_valid"=true order by id desc limit 1;'
            params = (self.token_str.get_secret_value(),)
        res = self.db.arbitrary(query, params) if query else None
        self.db.disconnect()
        return DBToken.from_row(res[0]) if res and len(res) > 0 else None

    def exists(self) -> bool:
        return self.token is not None and self.token.is_valid

    def invalidate(self):
        self.db.connect()
        res = self.db.arbitrary("UPDATE public.password_reset SET is_valid=false WHERE id = %s RETURNING *;",
                                (self.token.id,))
        if len(res) > 0:
            self.db.commit()
        else:
            self.db.rollback()
        self.db.disconnect()

    def add(self) -> bool:
        self.db.connect()
        res = self.db.arbitrary(
            'INSERT INTO public.password_reset (user_id) SELECT users.user_id FROM users WHERE users.email = %s RETURNING *;',
            (self.user.email,))[0]
        if res:
            self.db.commit()
            self.token = DBToken.from_row(res)
        else:
            self.db.rollback()
        self.db.disconnect()
        return res
