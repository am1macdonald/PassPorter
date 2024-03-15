from fastapi import Request
from fastapi.responses import RedirectResponse

from models.Authorization import Authorization
from models.Client import Client
from models.User import User


class Authorize:
    def __init__(self, request: Request, templates, conn):
        self.request = request
        self.templates = templates
        self._conn = conn
        self.client_id = request.query_params.get("client_id")
        self.redirect = request.query_params.get("redirect_uri")
        self.client = Client(self.client_id, conn=conn) if self.client_id else None
        self.db_client = self.client.get() if self.client else None
        self.user_token = self.request.cookies.get("token")

    def resolve_get(self):
        return self._resolve()

    def resolve_post(self, authorized):
        if authorized != "authorized":
            raise ValueError('not authorized')
        client_err = self._check_client()
        if client_err and client_err.get('error'):
            return client_err

        if not self.user_token:
            return self._redirect_to_sign_in()

        user = User(token=self.user_token, conn=self._conn)
        if user.get_user() is None:
            raise ValueError("User does not exist")

        auth = Authorization(conn=self._conn)
        auth_code = auth.add_authorization(user, self.client, self.request.query_params.get("redirect_uri"),
                                           self.request.query_params.get("scope"))
        redirect = self.request.query_params.get("redirect_uri")
        if auth_code and redirect:
            response = RedirectResponse(url=f"/redirect?authorization={auth_code}&redirect_uri={self.redirect}",
                                        status_code=303)
            return response

    def _resolve(self):
        client_err = self._check_client()
        if client_err and client_err.get('error'):
            return client_err

        if not self.user_token:
            return self._redirect_to_sign_in()

        return RedirectResponse(f"/consent?{self.request.query_params}", status_code=303)

    def _redirect_to_sign_in(self):
        url_string = f'/sign-in?{self.request.query_params}'
        return RedirectResponse(url=url_string)

    def _check_client(self):
        if not self.client:
            return {'error': True, 'message': 'client does not exist'}
        if self.redirect not in self.db_client.redirect:
            return {'error': True, 'message': 'invalid redirect'}
        return None
