from fastapi import FastAPI, Request
from pydantic import SecretStr, EmailStr

from controllers.DatabaseController import DatabaseController
from models.User import User


class SignupResolver:
    def __init__(self, email: EmailStr, password: SecretStr, confirm: SecretStr):
        print(email)
        print(password.get_secret_value())
        DatabaseController()
        User('bob', 'bobspass')
