import uuid
from datetime import datetime

import bcrypt
from pydantic import BaseModel, EmailStr, Field, SecretStr

from controllers.DatabaseController import DatabaseController


class DBModel(BaseModel):

    @classmethod
    def from_list(cls, tpl):
        return cls(**{k: v for k, v in zip(cls.__fields__.keys(), tpl)})
