from fastapi import Request
from fastapi.responses import RedirectResponse

from models.Authorization import Authorization
from models.Client import Client
from models.User import User


class RedirectResolver:
    def __init__(self, request: Request):
        self.request = request
        self.redirect = request.query_params.get("redirect_uri")
        self.auth_code = request.query_params.get("authorization")

    def resolve(self):
        return RedirectResponse(f"{self.redirect}?authorization={self.auth_code}", status_code=303)

