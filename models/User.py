import uuid
from datetime import datetime

import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from controllers.DatabaseController import DatabaseController


class NewUserInputModel(BaseModel):
    password: SecretStr = Field(min_length=8, max_length=100)
    email: EmailStr = Field()


class DBUser(BaseModel):
    username: str
    email: EmailStr
    password_hash: SecretStr
    last_login: datetime | None = None
    verification_status: bool
    attempts: int

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})


class UserRegistration:
    def __init__(self, email, password: SecretStr):
        self.email = email
        self.username = self._create_username(email)
        self.password = self._hash_password(password.get_secret_value())
        self.db = DatabaseController()

    @staticmethod
    def _hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def _create_username(email):
        return email.split('@')[0] + str(uuid.uuid4())

    def add(self):
        self.db.connect()
        user = self.db.insert('users', ['username', 'password_hash', 'email'],
                              (self.username, self.password, self.email))
        self.db.insert('email_verification',
                       ['user_id'], (user[0],))
        self.db.disconnect()


class UserLogin:
    def __init__(self, email: EmailStr):
        self.email = email
        self.db = DatabaseController()
        try:
            self.user = DBUser.from_list(self._fetch(email))
        except Exception as e:
            print(e)
            self.user = None

    def get_user(self) -> DBUser:
        return self.user

    def _fetch(self, email: EmailStr):
        self.db.connect()
        return self.db.arbitrary(f'''
        select
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
                ''', (email,))[0]
