import secrets

from pydantic import BaseModel

from controllers.DatabaseController import DatabaseController
from models.Authorization import DBAuth
from models.BaseDBModel import DBModel
from models.User import User


class TokenRequest(BaseModel):
    authorization: str
    client_secret: str
    client_id: str
