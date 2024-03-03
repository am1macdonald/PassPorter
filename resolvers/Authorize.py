from fastapi import Request
from fastapi.responses import RedirectResponse

from models.Authorization import Authorization
from models.Client import Client
from models.User import User


class Authorize:
    def __init__(self, request: Request, templates):
        self.request = request
        self.templates = templates
        self.client_id = request.query_params.get("client_id")
        self.redirect = request.query_params.get("redirect_uri")
        self.client = Client(self.client_id) if self.client_id else None
        self.db_client = self.client.get() if self.client else None
        self.user_token = self.request.cookies.get("token")

    def resolve_get(self, *args):
        client_err = self._check_client()
        if client_err and client_err.get('error'):
            return client_err

        if not self.user_token:
            url_string = f'/sign-in?{self.request.query_params}&next="{self.request.base_url}authorize"'
            response = RedirectResponse(url=url_string)
            return response

        return RedirectResponse(f"/consent?{self.request.query_params}", status_code=303)

    def resolve_post(self, authorized):
        if authorized != "authorized":
            raise ValueError('not authorized')
        client_err = self._check_client()
        if client_err and client_err.get('error'):
            return client_err

        if not self.user_token:
            url_string = f'/sign-in?{self.request.query_params}&next="{self.request.base_url}authorize"'
            response = RedirectResponse(url=url_string, status_code=303)
            return response

        user = User(token=self.user_token)
        if user.get_user() is None:
            raise ValueError("User does not exist")

        auth = Authorization(client_id=self.client_id)
        auth_code = auth.add_authorization(user, self.request.query_params.get("redirect_uri"),
                                           self.request.query_params.get("scope"))
        redirect = self.request.query_params.get("redirect_uri")
        if auth_code and redirect:
            response = RedirectResponse(url=f"/redirect?authorization={auth_code}&redirect_uri={self.redirect}",
                                        status_code=303)
            return response

    def _check_client(self):
        if not self.client:
            return {'error': True, 'message': 'client does not exist'}
        if self.redirect not in self.db_client.redirect:
            return {'error': True, 'message': 'invalid redirect'}
        return None
