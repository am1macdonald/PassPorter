from pydantic import EmailStr

from controllers.DatabaseController import DatabaseController


class PasswordReset:
    def __init__(self):
        self.db = DatabaseController()


