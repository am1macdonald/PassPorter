import uuid

import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from controllers.DatabaseController import DatabaseController


class NewUserInputModel(BaseModel):
    password: SecretStr
    email: EmailStr = Field()


class DBUser(BaseModel):
    print('')


class NewUser:
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
