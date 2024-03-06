import uuid
from datetime import datetime

import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from controllers.AuthController import AuthController
from models.BaseDBModel import DBModel


class NewUserInputModel(BaseModel):
    password: SecretStr = Field(min_length=8, max_length=100)
    email: EmailStr = Field()


class DBUser(DBModel):
    user_id: int
    username: str
    email: EmailStr
    password_hash: SecretStr
    last_login: datetime | None = None
    verification_status: bool
    attempts: int


class User:
    def __init__(self, email: str = None, password: SecretStr = None, user_id: int = None,
                 token=None, conn=None):
        self.email = email
        self.username = self._create_username(email) if email else None
        self.password = self._hash_password(password.get_secret_value()) if password else None
        self.user_id = user_id
        self.token = token
        self._conn = conn
        self.user: DBUser = self._fetch()

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _create_username(email):
        return email.split('@')[0] + str(uuid.uuid4())

    def add(self):
        cur = self._conn.cursor()
        sql = '''
        INSERT INTO public.users
        (username, password_hash, email)
        VALUES(%s,%s,%s)
        RETURNING *;
        '''
        vals = (self.username, self.password, self.email)
        cur.execute(sql, vals)
        res = cur.fetchone()
        if res:
            cur.commit()
            self.user = DBUser.from_row(res)

    def update_password(self, password: SecretStr):
        cur = self._conn.cursor()
        sql = '''
        UPDATE public.users
        SET password_hash=%s
        WHERE user_id=%s
        RETURNING password_hash; 
        '''
        vals = (self._hash_password(password.get_secret_value()), self.user.user_id,)
        cur.execute(sql, vals)
        res = cur.fetchone()
        if bcrypt.checkpw(password.get_secret_value().encode(), res[0].encode()):
            cur.commit()
            return True
        else:
            cur.rollback()
            return False

    def get_user(self):
        return self.user

    def get_token(self):
        return AuthController().issue_token(
            {"user_id": self.user.user_id, "email": self.user.email, "username": self.user.username})

    def _fetch(self):
        cur = self._conn.cursor()
        sql = ''
        vals = None
        if self.email:
            sql = f'''
            select
                users.user_id,
                users.username,
                users.email,
                users.password_hash,
                users.last_login,
                (
                select
                    email_verification.verification_status
                from
                    email_verification
                where
                    email_verification.user_id = users.user_id) as verification_status,
                (
                select
                    login_attempts.attempts
                from
                    login_attempts
                where
                    login_attempts.user_id = users.user_id) as attempts
            from
                users
            where
                users.email = %s
                    '''
            vals = (self.email,)
        elif self.user_id:
            sql = f'''
            select
                users.user_id,
                users.username,
                users.email,
                users.password_hash,
                users.last_login,
                (
                select
                    email_verification.verification_status
                from
                    email_verification
                where
                    email_verification.user_id = users.user_id) as verification_status,
                (
                select
                    login_attempts.attempts
                from
                    login_attempts
                where
                    login_attempts.user_id = users.user_id) as attempts
            from
                users
            where
                users.user_id = %s
                    '''
            vals = (self.user_id,)
        elif self.token:
            user_token = AuthController().decode_token(self.token)
            sql = f'''
            select
                users.user_id,
                users.username,
                users.email,
                users.password_hash,
                users.last_login,
                (
                select
                    email_verification.verification_status
                from
                    email_verification
                where
                    email_verification.user_id = users.user_id) as verification_status,
                (
                select
                    login_attempts.attempts
                from
                    login_attempts
                where
                    login_attempts.user_id = users.user_id) as attempts
            from
                users
            where
                users.email = %s
                    '''
            vals = (user_token.get("context").get("email"),)

        cur.execute(sql, vals)
        res = cur.fetchone()
        user = DBUser.from_row(res) if res else None
        return user
