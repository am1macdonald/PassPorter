from datetime import date

from fastapi import Request

from models.Authorization import Authorization
from models.Client import Client
from models.Token import TokenRequest
from models.User import User


class GetTokenResolver:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates

    def resolve(self, token_request: TokenRequest):
        auth = Authorization(token_request.authorization)
        db_auth = auth.get()
        if db_auth is None or db_auth.used or db_auth.expiration.date() < date.today():
            return {"error": "invalid authorization code"}
        client = Client(client_id=token_request.client_id)
        if not client.get():
            return {"error": "invalid client id"}
        if not client.validate(token_request.client_secret):
            return {"error": "invalid client secret"}
        user = User(user_id=db_auth.user_id)
        token = user.get_token()
        if auth.mark_used() is None:
            raise ValueError("can\'t use token")
        return {'token': token}
